"""路由分发模块"""
import re
from typing import Dict, Callable, Optional, Any, Tuple
from http.server import BaseHTTPRequestHandler


class Route:
    """路由定义"""

    def __init__(self, method: str, path_pattern: str, handler: Callable):
        self.method = method
        self.path_pattern = path_pattern
        self.handler = handler
        # 编译正则表达式
        self.regex = re.compile(path_pattern)

    def match(self, method: str, path: str) -> Optional[Tuple[Any, ...]]:
        """匹配路由"""
        if self.method.upper() != method.upper():
            return None

        match = self.regex.match(path)
        if match:
            return match.groups()
        return None


class Router:
    """路由器"""

    def __init__(self):
        self.routes: list[Route] = []

    def add_route(self, method: str, path: str, handler: Callable) -> None:
        """添加路由"""
        # 将路径参数转换为正则表达式
        # 例如 /books/{id} -> /books/(?P<id>\d+)
        pattern = path
        param_names = []

        # 查找 {param} 格式的参数
        param_pattern = re.compile(r'\{(\w+)\}')
        for match in param_pattern.finditer(path):
            param_name = match.group(1)
            param_names.append(param_name)

        # 替换参数为正则模式
        pattern = param_pattern.sub(r'([^/]+)', pattern)
        pattern = f'^{pattern}$'

        self.routes.append(Route(method, pattern, handler))

    def route(self, method: str, path: str) -> Optional[Tuple[Callable, Tuple[Any, ...]]]:
        """查找匹配的路由"""
        # 去掉查询字符串
        path = path.split('?')[0]

        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route.handler, params

        return None

    def get(self, path: str) -> Callable:
        """GET 路由装饰器"""
        def decorator(handler: Callable) -> Callable:
            self.add_route('GET', path, handler)
            return handler
        return decorator

    def post(self, path: str) -> Callable:
        """POST 路由装饰器"""
        def decorator(handler: Callable) -> Callable:
            self.add_route('POST', path, handler)
            return handler
        return decorator

    def put(self, path: str) -> Callable:
        """PUT 路由装饰器"""
        def decorator(handler: Callable) -> Callable:
            self.add_route('PUT', path, handler)
            return handler
        return decorator

    def patch(self, path: str) -> Callable:
        """PATCH 路由装饰器"""
        def decorator(handler: Callable) -> Callable:
            self.add_route('PATCH', path, handler)
            return handler
        return decorator

    def delete(self, path: str) -> Callable:
        """DELETE 路由装饰器"""
        def decorator(handler: Callable) -> Callable:
            self.add_route('DELETE', path, handler)
            return handler
        return decorator


# 全局路由器实例
router = Router()
