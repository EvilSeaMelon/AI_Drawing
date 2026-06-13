import json
import os
from utils.path_tool import get_abs_path

class ComponentRAG:
    def __init__(self):
        self.library = {}
        self._load_data()

    def _load_data(self):
        file_path = get_abs_path("data/components.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.library = json.load(f)

    def retrieve(self, user_query: str) -> dict:
        """
        基于简单的关键词匹配进行检索
        如果用户的语音里包含了我们知识库里的实体，就把它召回。
        """
        retrieved_templates = {}
        for key, template in self.library.items():
            if key in user_query:
                retrieved_templates[key] = template
        return retrieved_templates

# 全局单例
rag_engine = ComponentRAG()