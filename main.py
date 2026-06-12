import uvicorn
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from utils.database import Base, engine, get_db
from models.models import CanvasState
from schemas.payload import CommandRequest
from agent.core import process_voice_command

# 启动时自动创建MySQL数据表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI_Painter Backend",
    description="FastAPI service for pure voice-controlled canvas agent",
    version="1.0.0",
)

# 配置跨域，保证前端Canvas页面可以直接调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _api_response(code: int, message: str, data: Optional[dict] = None) -> dict:
    """统一的 API 响应格式"""
    return {
        "code": code,
        "message": message,
        "data": data or {},
    }


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AI Voice Painter Backend is running!"}


@app.post("/api/command")
async def process_command_endpoint(request: CommandRequest, db: Session = Depends(get_db)):
    """
    核心端点：接收前端语音转换后的文本指令，交给大模型拆解为绘图动作
    """
    print(f"\n[API] Command request received -> session_id={request.session_id}, text={request.text_command}")

    try:
        result = process_voice_command(
            session_id=request.session_id,
            text_command=request.text_command,
            db=db
        )

        return _api_response(
            code=200,
            message="success",
            data={
                "session_id": request.session_id,
                "actions": result["actions"],
                "message": result["message"]
            }
        )
    except Exception as e:
        print(f"[API] Command error: {e}")
        return _api_response(code=500, message=f"server_error: {str(e)}")


if __name__ == "__main__":
    # 使用 uvicorn 启动服务
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)