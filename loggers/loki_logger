import os
import yaml
import logging
from logging_loki import LokiHandler


def init_loki() -> LokiHandler:
    logger_path = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(logger_path, 'promtail-config.yaml')

    with open(file=yaml_path, mode='r', encoding='utf-8') as file:
        compose_data = yaml.safe_load(file)

    loki_url = compose_data['clients'][0]['url']

    loki_handler = LokiHandler(
        url=loki_url,
        tags={'service_name': 'loki_logger'},
        version='1',
    )
    formatter = logging.Formatter(fmt=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
    loki_handler.setFormatter(formatter)

    return loki_handler
