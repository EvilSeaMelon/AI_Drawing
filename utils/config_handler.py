import yaml
from utils.path_tool import get_abs_path

def load_db_config(config_path: str=get_abs_path("config/db.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    try:
        with open(config_path, "r", encoding=encoding) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        return {}

db_conf = load_db_config()
agent_conf = load_agent_config()