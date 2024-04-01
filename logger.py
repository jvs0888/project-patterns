import os
from loguru import logger
from datetime import datetime


class LoggerMixin:
    def __init__(self):
        self.classname = self.__class__.__name__
        self.date = datetime.now().date()
        self.logger = logger.bind(classname=self.classname)
        self.path = os.path.join(os.path.dirname(__file__), 'logs', f'{self.date}.log')
        self.logger.add(sink=self.path,
                        backtrace=True,
                        diagnose=True,
                        encoding='utf-8',
                        rotation='5 MB')
