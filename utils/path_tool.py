import os
from pathlib import Path

def get_abs_path(relative_path: str) -> str:
    """获取项目根目录下的绝对路径"""
    base_dir = Path(__file__).resolve().parent.parent
    return str(base_dir / relative_path)