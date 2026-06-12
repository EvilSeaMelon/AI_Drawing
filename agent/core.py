import json
from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import List

from models.models import CanvasState, TokenLog
from schemas.payload import DrawAction
from utils.llm_factory import chat_model
from utils.config_handler import agent_conf

# 定义一个大模型专属的输出结构（供 LangChain 解析）
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
        # 如果是新会话，初始化一个空画布状态并保存
        canvas = CanvasState(session_id=session_id, current_shapes="[]")
        db.add(canvas)
        db.commit()
        db.refresh(canvas)  # 刷新以获取最新状态

    # 解析出当前的图形列表，准备喂给大模型
    current_context = json.loads(canvas.current_shapes)

    # ==========================================
    # 2. 组装 Prompt
    # ==========================================
    system_prompt = agent_conf.get("prompts", {}).get("system_template", "你是一个绘图助手。")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_input}")
    ])

    # 格式化 Prompt，注入当前画布状态
    messages = prompt_template.format_messages(
        canvas_state=current_context,
        user_input=text_command
    )

    # ==========================================
    # 3. 核心大模型调用 (利用 with_structured_output 强制输出 AgentOutput 结构)
    # ==========================================
    structured_llm = chat_model.with_structured_output(AgentOutput)

    print(f"[Agent] 正在思考并请求大模型，指令: '{text_command}'...")

    # 获取结构化结果 (AgentOutput对象)
    ai_result: AgentOutput = structured_llm.invoke(messages)

    # ==========================================
    # 4. 更新 MySQL 中的画布状态
    # ==========================================
    # 兼容处理：防止 SQLAlchemy 已经将其自动解析为 list
    if isinstance(current_context, str):
        current_context_list = json.loads(current_context)
    elif isinstance(current_context, list):
        current_context_list = current_context
    else:
        current_context_list = []

    # 将新的动作序列化后追加进去
    for action in ai_result.actions:
        current_context_list.append(action.model_dump())

    canvas.current_shapes = json.dumps(current_context_list, ensure_ascii=False)

    # ==========================================
    # 5. 记录 Token 流水与成本
    # ==========================================
    # 可以通过LangChain的callback机制精准捕获Token，先使用模拟计算处理
    estimated_prompt_tokens = len(system_prompt) + len(current_context) + len(text_command)
    estimated_completion_tokens = len(str(ai_result.model_dump()))

    token_log = TokenLog(
        session_id=session_id,
        prompt_tokens=estimated_prompt_tokens,
        completion_tokens=estimated_completion_tokens,
        total_tokens=estimated_prompt_tokens + estimated_completion_tokens,
        estimated_cost=(estimated_prompt_tokens + estimated_completion_tokens) * 0.00002
    )
    db.add(token_log)
    db.commit()

    return {
        "actions": [a.model_dump() for a in ai_result.actions],
        "message": ai_result.message
    }
