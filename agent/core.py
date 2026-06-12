import json
from sqlalchemy.orm import Session
from models.models import CanvasState, TokenLog
from schemas.payload import DrawAction


def process_voice_command(session_id: str, text_command: str, db: Session) -> dict:
    """
    处理用户语音指令的核心Agent
    操作数据库模型
    """
    # ==========================================
    # 1.读取历史状态
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
    # 2.调用大模型Agen（此处先做 Mock 模拟）
    # ==========================================
    print(f"[Agent] 收到指令: '{text_command}' | 当前画布状态: {current_context}")

    # TODO: 下一阶段我们将在这里接入通义千问/OpenAI 的 Function Calling
    # 假设 AI 分析指令后，决定画一个红色的圆
    mock_action = DrawAction(
        action="draw_circle",
        params={"x": 200, "y": 200, "radius": 50, "color": "red"}
    )

    # 模拟大模型返回的 Token 消耗
    mock_prompt_tokens = 150
    mock_completion_tokens = 45

    # ==========================================
    # 3.AI 处理后，更新画布状态
    # ==========================================
    # 将新的动作追加到画布状态中
    current_context.append(mock_action.model_dump())

    # 将更新后的 JSON 字符串写回数据库模型
    canvas.current_shapes = json.dumps(current_context, ensure_ascii=False)

    # ==========================================
    # 4.记录运营成本流水
    # ==========================================
    # 创建 Token 消耗记录
    token_log = TokenLog(
        session_id=session_id,
        prompt_tokens=mock_prompt_tokens,
        completion_tokens=mock_completion_tokens,
        total_tokens=mock_prompt_tokens + mock_completion_tokens,
        estimated_cost=(mock_prompt_tokens + mock_completion_tokens) * 0.00002  # 假设单价
    )
    db.add(token_log)

    # 最后统一提交事务，保证状态和日志同时写入成功！
    db.commit()

    return {
        "actions": [mock_action.model_dump()],
        "message": "绘制完毕。"
    }
