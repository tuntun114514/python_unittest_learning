import yaml
from pathlib import  Path

class ConfigError(Exception):
    """配制错误基类"""
    pass
class Config:
    def __init__(self,path):
        self.path = Path(path)
        if not self.path.exists():
            raise ConfigError(f"配置文件不存在：{self.path}")

        with open(self.path,'r',encoding='utf-8')as f:
            self.data = yaml.safe_load(f)
        self.validate()

    def validate(self):
        """验证配置格式"""
        if 'version' not in self.data:
            raise ConfigError("配置缺少必填字段: version")

    def get_version(self):
        return  self.data.get('version')
