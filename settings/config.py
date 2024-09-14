import os
import json
from dotenv import load_dotenv

try:
    from decorators.utils import utils
except ImportError as ie:
    exit(ie)


class Config:
    def __init__(self):
        self.config_path = os.path.dirname(os.path.abspath(__file__))
        self.project_path = os.path.dirname(self.config_path)
        self.env_path = os.path.join(self.config_path, '.env')
        self.read_config()
        load_dotenv(dotenv_path=self.env_path)

    def __getattr__(self, attr: str) -> str:
        return os.getenv(attr)

    @utils.exception
    def read_config(self) -> None:
        files = [file for file in os.listdir(self.config_path) if file.endswith('.json')]
        for file in files:
            file_path = os.path.join(self.config_path, file)
            with open(file=file_path, mode='r', encoding='utf-8') as cfg:
                setattr(self, file[:-5], json.loads(cfg.read()))


config = Config()
