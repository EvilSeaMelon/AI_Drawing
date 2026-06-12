
"""
统一管理大模型实例，大模型底层默认自动读取 DASHSCOPE_API_KEY 环境变量。
"""

from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import agent_conf

class ChatModelFactory:
    """实例化通义千问"""
    @staticmethod
    def create_chat_model() -> ChatTongyi:
        llm_config = agent_conf.get("llm", {})
        return ChatTongyi(
            model=llm_config.get("model_name", "qwen3-max"),
            temperature=llm_config.get("temperature", 0.1)
        )

# 全局单例
chat_model = ChatModelFactory.create_chat_model()