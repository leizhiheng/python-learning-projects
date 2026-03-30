"""日志中间件"""
import logging
import time
from typing import Callable
from http.server import BaseHTTPRequestHandler
from config import Config


# 配置日志
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


def log_request(handler_func: Callable) -> Callable:
    """记录请求日志的装饰器"""
    def wrapper(self: BaseHTTPRequestHandler, *args, **kwargs):
        start_time = time.time()

        # 执行请求处理
        try:
            result = handler_func(self, *args, **kwargs)
            status = self._status_code if hasattr(self, '_status_code') else 200
            return result
        except Exception as e:
            status = 500
            raise
        finally:
            # 记录日志
            duration = time.time() - start_time
            log_message = (
                f"{self.command} {self.path} - "
                f"{status} - {duration:.3f}s"
            )
            if status >= 500:
                logger.error(log_message)
            elif status >= 400:
                logger.warning(log_message)
            else:
                logger.info(log_message)

    return wrapper
