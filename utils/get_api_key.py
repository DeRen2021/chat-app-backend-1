import os
import logging
from typing import Optional
from dotenv import load_dotenv
from google.cloud import secretmanager
import boto3
from botocore.exceptions import ClientError

# 加载本地 .env 文件
load_dotenv()

logger = logging.getLogger(__name__)

# API密钥名称常量
OPENAI_KEY_NAME = "OPENAI_API_KEY"
ANTHROPIC_KEY_NAME = "ANTHROPIC_API_KEY"
DEEPSEEK_KEY_NAME = "DEEPSEEK_API_KEY"

AWS_KEY_NAME = "AWS_ACCESS_KEY"
AWS_SECRET_NAME = "AWS_SECRET_KEY"



class APIKeyManager:
    def __init__(self):
        self._cached_keys = {}  # 缓存获取到的密钥
        
    def _get_from_local_env(self, key_name: str) -> Optional[str]:
        """从本地 .env 文件获取密钥"""
        value = os.getenv(key_name)
        if value:
            logger.info(f"Successfully loaded {key_name} from local .env")
        return value

    def _get_from_env(self, key_name: str) -> Optional[str]:
        """从环境变量获取密钥"""
        return os.getenv(key_name)

    # def _get_from_aws_secrets(self, secret_name: str) -> Optional[str]:
    #     """从AWS Secrets Manager获取密钥"""
    #     try:
    #         session = boto3.session.Session()
    #         client = session.client(
    #             service_name='secretsmanager',
    #             region_name='us-east-1'
    #         )
    #         response = client.get_secret_value(SecretId=secret_name)
    #         return response['SecretString']
    #     except Exception as e:
    #         logger.error(f"AWS Secrets error: {e}")
    #         return None

    # def _get_from_gcp_secrets(self, secret_name: str) -> Optional[str]:
    #     """从Google Cloud Secret Manager获取密钥"""
    #     try:
    #         project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    #         if not project_id:
    #             return None
                
    #         client = secretmanager.SecretManagerServiceClient()
    #         name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    #         response = client.access_secret_version(request={"name": name})
    #         return response.payload.data.decode("UTF-8")
    #     except Exception as e:
    #         logger.debug(f"GCP Secret Manager error: {e}")
    #         return None

    def get_secret(self, key_name: str) -> str:
        """
        按优先级获取密钥：
        1. 缓存
        2. 本地 .env 文件
        3. 环境变量
        4. AWS Secrets Manager
        5. GCP Secret Manager
        """
        # 如果已经缓存，直接返回
        if key_name in self._cached_keys:
            return self._cached_keys[key_name]

        # 按顺序尝试不同的获取方式
        secret_value = None
        
        # 1. 本地 .env 文件
        secret_value = self._get_from_local_env(key_name)
        if secret_value:
            logger.info(f"Found {key_name} in local .env file")
            self._cached_keys[key_name] = secret_value
            return secret_value

        # 2. 环境变量
        secret_value = self._get_from_env(key_name)
        if secret_value:
            logger.info(f"Found {key_name} in environment variables")
            self._cached_keys[key_name] = secret_value
            return secret_value

        # 3. AWS Secrets Manager
        # secret_value = self._get_from_aws_secrets(key_name)
        # if secret_value:
        #     logger.info(f"Found {key_name} in AWS Secrets Manager")
        #     self._cached_keys[key_name] = secret_value
        #     return secret_value

        # # 4. GCP Secret Manager
        # secret_value = self._get_from_gcp_secrets(key_name)
        # if secret_value:
        #     logger.info(f"Found {key_name} in GCP Secret Manager")
        #     self._cached_keys[key_name] = secret_value
        #     return secret_value

        # 如果所有方式都失败
        logger.error(f"Failed to get {key_name} from any source")
        raise ValueError(f"Could not find {key_name} in any configuration source")

# 创建单例实例
_api_key_manager = APIKeyManager()

# 导出可直接使用的函数
def get_openai_key() -> str:
    return _api_key_manager.get_secret(OPENAI_KEY_NAME)

def get_anthropic_key() -> str:
    return _api_key_manager.get_secret(ANTHROPIC_KEY_NAME)

def get_deepseek_key() -> str:
    return _api_key_manager.get_secret(DEEPSEEK_KEY_NAME)

def get_aws_key() -> str:
    return _api_key_manager.get_secret(AWS_KEY_NAME)

def get_aws_secret() -> str:
    return _api_key_manager.get_secret(AWS_SECRET_NAME)

# 也可以选择导出实例本身
api_key_manager = _api_key_manager
