# api/openai_api.py
import logging
from typing import List
import openai
from utils.get_api_key import get_openai_key
from schemas.chat import Message

logger = logging.getLogger(__name__)

class OpenAIHandler:
    def __init__(self):
        try:
            self.api_key = get_openai_key()
            self.client = openai.OpenAI(api_key=self.api_key)
            self.default_model = "gpt-4o"
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise

    async def chat_completion(self, messages: List[Message],) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=messages,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise