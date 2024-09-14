import inspect
import paramiko
import functools
import psycopg2
import psycopg2.extras
import psycopg2.extensions
from time import sleep

try:
    from loggers.logger import logger
    from settings.config import config
except ImportError as ie:
    exit(ie)


class Connection:
    @staticmethod
    def get_connection(connect_to: str) -> paramiko.transport.Transport | psycopg2.extensions.connection:
        for _ in range(5):
            try:
                if connect_to == 'sftp':
                    transport = paramiko.Transport((config.SFTP_HOST, int(config.SFTP_PORT)))
                    transport.connect(username=config.SFTP_USER, password=config.SFTP_PASS)
                    return transport
                elif connect_to == 'db':
                    connect = psycopg2.connect(config.db['connection_link_local'])
                    return connect
            except Exception as e:
                logger.error(f'connection exception :: {e}')
                sleep(1)
                continue

        logger.error(f'maximum connection attempts has been reached')

    def sftp(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            transport, sftp_client = None, None
            try:
                transport = self.get_connection(connect_to='sftp')
                if not transport:
                    logger.error(f'failed to establish sftp connection')
                    return False

                sftp_client = paramiko.SFTPClient.from_transport(transport)
                kwargs['sftp_client'] = sftp_client
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'exception in "{func.__name__}" => {e}')
            finally:
                sftp_client.close() if sftp_client else None
                transport.close() if transport else None
        return wrapper

    def cursor(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            connect, cursor = None, None
            try:
                connect = self.get_connection(connect_to='db')
                if not connect:
                    logger.error(f'failed to establish database connection')
                    return False

                cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                arguments = inspect.getfullargspec(func).args
                if 'connect' in arguments:
                    kwargs['connect'] = connect

                kwargs['cursor'] = cursor
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'exception in "{func.__name__}" => {e}')
            finally:
                connect.close() if connect else None
                cursor.close() if cursor else None
        return wrapper


connection = Connection()
