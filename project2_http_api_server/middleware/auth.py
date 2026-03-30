"""认证中间件"""
import functools
from typing import Callable, Dict, Any, Optional
from http.server import BaseHTTPRequestHandler
from utils.jwt import verify_token


def get_token_from_header(auth_header: Optional[str]) -> Optional[str]:
    """从 Authorization header 提取 token"""
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2:
        return None

    scheme, token = parts
    if scheme.lower() != 'bearer':
        return None

    return token


def require_auth(handler_func: Callable) -> Callable:
    """要求认证的装饰器"""
    @functools.wraps(handler_func)
    def wrapper(self: BaseHTTPRequestHandler, *args, **kwargs):
        auth_header = self.headers.get('Authorization')
        token = get_token_from_header(auth_header)

        if not token:
            return self.send_error_response(401, "UNAUTHORIZED", "未提供认证信息")

        payload = verify_token(token)
        if not payload:
            return self.send_error_response(401, "UNAUTHORIZED", "Token 无效或已过期")

        # 将用户信息存储到请求对象
        self.current_user = payload
        return handler_func(self, *args, **kwargs)

    return wrapper


def optional_auth(handler_func: Callable) -> Callable:
    """可选认证的装饰器"""
    @functools.wraps(handler_func)
    def wrapper(self: BaseHTTPRequestHandler, *args, **kwargs):
        auth_header = self.headers.get('Authorization')
        token = get_token_from_header(auth_header)

        if token:
            payload = verify_token(token)
            if payload:
                self.current_user = payload
            else:
                self.current_user = None
        else:
            self.current_user = None

        return handler_func(self, *args, **kwargs)

    return wrapper
