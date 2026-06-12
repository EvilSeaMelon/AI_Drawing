from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from utils.database import Base

class CanvasState(Base):
    """
    画布状态表：通过 Session ID 唯一绑定，
    仅保存最新的画布 JSON 状态，实现大模型上下文的“滑动窗口”截断机制。
    """
    __tablename__ = "canvas_states"

    session_id = Column(String(50), primary_key=True, index=True, comment="会话唯一标识")
    current_shapes = Column(Text, default="[]", comment="当前画布所有图形的 JSON 字符串")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="最后更新时间")
