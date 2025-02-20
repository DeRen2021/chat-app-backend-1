import logging
from typing import Optional,List
import anthropic
from utils.get_api_key import get_anthropic_key
from schemas.chat import Message
logger = logging.getLogger(__name__)

class AnthropicHandler:
    def __init__(self):
        try:
            self.api_key = get_anthropic_key()
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.default_model = "claude-3-5-sonnet-20241022"
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise

    async def chat_completion(
        self, 
        messages: list[Message], 
    ) -> str:
        try:
            # 
            response = self.client.messages.create(
                model=self.default_model,
                max_tokens=4096,
                messages=messages
            )

            # 
            return response.content[0].text

        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in chat_completion: {e}")
            raise

