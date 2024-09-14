import asyncio
import functools
from time import time, sleep
from playwright.async_api import async_playwright

try:
    from loggers.logger import logger
except ImportError as ie:
    exit(ie)


class Timer:
    def __init__(self):
        self.start_time = None
        self.runtime = float()

    def __enter__(self):
        self.start_time = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.runtime = time() - self.start_time

    def get_runtime(self):
        if self.runtime > 3600:
            runtime = f'{str(round(self.runtime / 3600, 2))} hours'
            logger.info(f'runtime :: {runtime}')
        elif self.runtime > 60:
            runtime = f'{str(round(self.runtime / 60, 2))} minutes'
            logger.info(f'runtime :: {runtime}')
        else:
            runtime = f'{str(round(self.runtime, 2))} seconds'
            logger.info(f'runtime :: {runtime} seconds')

        return runtime

class Utils(Timer):
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def retry(retries: int = 3, delay: int = 1):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        logger.exception(f'exception in "{func.__name__}" => {e}')
                    if attempt < retries - 1:
                        logger.info('retrying')
                        sleep(delay)
                logger.error('max retries exceeded')
                return False
            return wrapper
        return decorator

    @staticmethod
    def async_retry(retries: int = 3, delay: int = 1):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                for attempt in range(retries):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        logger.exception(f'exception in "{func.__name__}" => {e}')
                    if attempt < retries - 1:
                        logger.info('retrying')
                        await asyncio.sleep(delay)
                logger.error('max retries exceeded')
                return False
            return wrapper
        return decorator

    @staticmethod
    def exception(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'exception in "{func.__name__}" => {e}')
                return False
        return wrapper

    @staticmethod
    def async_exception(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'exception in "{func.__name__}" => {e}')
                return False
        return wrapper

    def timer(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.start_time = time()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'exception in "{func.__name__}" => {e}')
            finally:
                self.runtime = time() - self.start_time
                self.get_runtime()
        return wrapper

    def async_timer(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            self.start_time = time()
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'exception in "{func.__name__}" => {e}')
            finally:
                self.runtime = time() - self.start_time
                self.get_runtime()
        return wrapper

    @staticmethod
    def playwright_initiator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            playwright_context = await async_playwright().start()
            try:
                kwargs['playwright'] = playwright_context
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'exception in "{func.__name__}" => {e}')
                return False
            finally:
                await playwright_context.stop()
        return wrapper


utils = Utils()
