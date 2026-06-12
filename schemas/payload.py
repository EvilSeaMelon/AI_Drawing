from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CommandRequest(BaseModel):
    """前端传给后端的语音绘图指令"""
    session_id: str = Field(..., description="当前绘图会话的唯一标识")
    text_command: str = Field(..., description="语音转录后的文本指令")

class DrawAction(BaseModel):
    """拆解后的具体绘图动作 (发给前端 Canvas 执行)"""
    action: str = Field(..., description="执行的动作，如 draw_circle, modify_color")
    params: Dict[str, Any] = Field(default_factory=dict, description="动作参数字典")

class CommandResponse(BaseModel):
    """后端返回的标准结构"""
    session_id: str
    success: bool
    actions: List[DrawAction]
    message: str = Field(..., description="AI的回复语，可用于前端语音播报")