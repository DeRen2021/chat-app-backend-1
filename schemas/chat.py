from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import List

class RoleEnum(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class ModelEnum(str, Enum):
    gpt_4o = "gpt-4o"
    claude_3_5 = "claude-3-5-sonnet-20241022"
    deepseek_chat = "deepseek-chat"

class Message(BaseModel):
    role: RoleEnum = Field(..., description="allowed roles: system, user")
    content: str = Field(..., description="messages")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="list of messages")
    model: ModelEnum = Field(
        default=ModelEnum.deepseek_chat, description="language model"
    )
    
class ChatResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    response: str = Field(..., description="response from language model")
    model_used: ModelEnum = Field(..., description="llm that been used")