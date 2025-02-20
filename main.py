from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from api.openai_api import OpenAIHandler
from api.anthropic_api import AnthropicHandler
from api.deepseek_api import DeepSeekHandler
from schemas.chat import ChatRequest, ChatResponse
import logging


# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title ="Chat API", description="backend api for openai, anthropic, deepseek")



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://chat.deren.life",
#                    "http://chat.deren.life",
#                    "http://localhost",
#                    "http://127.0.0.1"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（仅用于开发环境）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)



openai_handler = OpenAIHandler()
anthropic_handler = AnthropicHandler()
deepseek_handler = DeepSeekHandler()

@app.get("/")
async def root():
    """健康检查接口"""
    return {"status": "ok", "message": "API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        messages = request.messages
        logger.info(f"Received chat request with model: {request.model}")
        logger.info(f"Received chat request with messages: {messages}")
        if not messages:
            raise HTTPException(status_code=400, detail="Messages list is empty")
            
        model = request.model
        logger.info(f"Received chat request with model: {model}")

        if "gpt" in model:
            response = await openai_handler.chat_completion(messages)
        elif "claude" in model:
            response = await anthropic_handler.chat_completion(messages)
        elif "deepseek" in model:
            response = await deepseek_handler.chat_completion(messages)


        return ChatResponse(response=response, model_used=model)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))