import uvicorn
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from utils.database import Base, engine, get_db
from models.models import CanvasState, TokenLog
from schemas.payload import CommandRequest

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
    """统一的 API 响应格式，对齐项目原有规范"""
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
        # TODO: 这里将在下一步接入大模型的 Agent 逻辑

        # 临时 mock 返回数据
        mock_actions = [
            {"action": "draw_circle", "params": {"x": 200, "y": 200, "radius": 50, "color": "blue"}}
        ]
        ai_message = "好的，我已经在画布中央为您画了一个蓝色的圆。"

        return _api_response(
            code=200,
            message="success",
            data={
                "session_id": request.session_id,
                "actions": mock_actions,
                "message": ai_message
            }
        )
    except Exception as e:
        print(f"[API] Command error: {e}")
        return _api_response(code=500, message=f"server_error: {str(e)}")


if __name__ == "__main__":
    # 使用 uvicorn 启动服务
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)