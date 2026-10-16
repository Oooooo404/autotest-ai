import yaml
import os

def load():
    """加载config.yaml，返回当前环境的配置"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"config.yaml")
    with open(config_path,"r",encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
        return cfg[cfg["env"]]
