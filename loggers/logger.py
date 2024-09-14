import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler


def init_logger(name: str = 'logger',
                file_log: bool = False,
                stream_log: bool = True,
                rotate: bool = False) -> logging.Logger:

    log_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    if not os.path.exists(log_directory):
        try:
            os.makedirs(log_directory)
        except Exception as e:
            print(f'failed to create log directory on a path :: {log_directory} :: {e}')
            exit()

    log_filename = f'{name}_{str(datetime.now().date())}.log'
    log_filepath = os.path.join(log_directory, log_filename)

    logger = logging.getLogger(name)
    level = logging.INFO
    logger.setLevel(level)
    formatter = logging.Formatter(fmt=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

    if file_log:
        if rotate:
            file_handler = RotatingFileHandler(log_filepath,
                                               maxBytes=1000000,
                                               backupCount=1)
        else:
            file_handler = logging.FileHandler(log_filepath)

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if stream_log:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


logger = init_logger()
