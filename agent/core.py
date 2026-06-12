import json
from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

# 移除了 TokenLog 的导入
from models.models import CanvasState
from schemas.payload import DrawAction
from utils.llm_factory import chat_model
from utils.config_handler import agent_conf


# 定义一个大模型专属的输出结构
class AgentOutput(BaseModel):
    actions: List[DrawAction] = Field(description="拆解出的绘图动作列表，按顺序执行")
    message: str = Field(description="AI 用自然语言给用户的回复语，例如'已为您在中间画了一个红色的圆'")


def process_voice_command(session_id: str, text_command: str, db: Session) -> dict:
    """
    处理用户语音指令的核心Agent
    """
    # ==========================================
    # 1. 从 MySQL 拉取最新的画布状态
    # ==========================================
    canvas = db.query(CanvasState).filter(CanvasState.session_id == session_id).first()

    if not canvas:
        canvas = CanvasState(session_id=session_id, current_shapes="[]")
        db.add(canvas)
        db.commit()
        db.refresh(canvas)

    current_context = json.loads(canvas.current_shapes)

    # ==========================================
    # 2. 组装 Prompt
    # ==========================================
    system_prompt = agent_conf.get("prompts", {}).get("system_template", "你是一个绘图助手。")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_input}")
    ])

    messages = prompt_template.format_messages(
        canvas_state=current_context,
        user_input=text_command
    )

    # ==========================================
    # 3. 核心大模型调用
    # ==========================================
    structured_llm = chat_model.with_structured_output(AgentOutput)
    print(f"[Agent] 正在思考并拆解复杂指令: '{text_command}'...")
    ai_result: AgentOutput = structured_llm.invoke(messages)

    # ==========================================
    # 4. 更新 MySQL 中的画布状态
    # ==========================================
    if isinstance(current_context, str):
        current_context_list = json.loads(current_context)
    elif isinstance(current_context, list):
        current_context_list = current_context
    else:
        current_context_list = []

    for action in ai_result.actions:
        current_context_list.append(action.model_dump())

    canvas.current_shapes = json.dumps(current_context_list, ensure_ascii=False)

    # 直接提交画布更新即可，无需再记录 Token
    db.commit()

    return {
        "actions": [a.model_dump() for a in ai_result.actions],
        "message": ai_result.message
    }