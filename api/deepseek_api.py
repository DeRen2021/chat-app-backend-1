from typing import List
import openai
from utils.get_api_key import get_deepseek_key
from schemas.chat import Message


class DeepSeekHandler:
    def __init__(self):
        """初始化 OpenAI 客户端"""
        try:
            self.api_key = get_deepseek_key()
            #self.client = openai.OpenAI(api_key=self.api_key)
            self.client = openai.OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
            self.default_model = "deepseek-chat"
        except Exception as e:
            raise

    async def chat_completion(self, messages: List[Message]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=messages,
                stream=False
            )

            return response.choices[0].message.content

        except Exception as e:
            raise