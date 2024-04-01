import os
import json
import random
from dotenv import load_dotenv


class Config:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.env_path = os.path.join(self.path, '.env')
        self.proxies = self.read_proxies()
        load_dotenv(dotenv_path=self.env_path)

    def __getattr__(self, attr):
        if attr == 'PROXY':
            return random.choice(self.proxies)
        if attr == 'DB_CONNECT':
            return json.loads(os.getenv(attr))
        return os.getenv(attr)

    def read_proxies(self):
        proxies_path = os.path.join(self.path, 'proxies.json')
        with open(file=proxies_path, mode='r', encoding='utf-8') as file:
            proxies = json.loads(file.read())
        return proxies
