"""错误处理中间件"""
import json
import traceback
from typing import Callable, Dict, Any
from http.server import BaseHTTPRequestHandler


class APIError(Exception):
    """API 错误基类"""
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


class NotFoundError(APIError):
    """404 错误"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(404, "NOT_FOUND", message)


class BadRequestError(APIError):
    """400 错误"""
    def __init__(self, message: str = "请求参数错误"):
        super().__init__(400, "BAD_REQUEST", message)


class UnauthorizedError(APIError):
    """401 错误"""
    def __init__(self, message: str = "未授权"):
        super().__init__(401, "UNAUTHORIZED", message)


class ForbiddenError(APIError):
    """403 错误"""
    def __init__(self, message: str = "禁止访问"):
        super().__init__(403, "FORBIDDEN", message)


class ConflictError(APIError):
    """409 错误"""
    def __init__(self, message: str = "资源冲突"):
        super().__init__(409, "CONFLICT", message)


def handle_errors(handler_func: Callable) -> Callable:
    """统一错误处理装饰器"""
    def wrapper(self: BaseHTTPRequestHandler, *args, **kwargs):
        try:
            return handler_func(self, *args, **kwargs)
        except APIError as e:
            self.send_json_response(e.status_code, {
                "success": False,
                "error": {
                    "code": e.code,
                    "message": e.message
                }
            })
        except Exception as e:
            # 记录完整堆栈
            traceback.print_exc()
            self.send_json_response(500, {
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "服务器内部错误"
                }
            })

    return wrapper
