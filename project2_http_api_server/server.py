"""HTTP 服务器实现"""
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional, Tuple
from urllib.parse import parse_qs

from config import Config
from router import router
from middleware import log_request, handle_errors, logger
from middleware.auth import require_auth
from handlers import AuthHandler, BookHandler, UserHandler
from utils.db import db


class APIHandler(BaseHTTPRequestHandler):
    """API 请求处理器"""

    # 路由映射
    HANDLERS = {
        'auth': AuthHandler,
        'book': BookHandler,
        'user': UserHandler,
    }

    def log_message(self, format, *args):
        """禁用默认日志输出"""
        pass

    def send_json_response(self, status_code: int, data: Dict[str, Any]) -> None:
        """发送 JSON 响应"""
        self._status_code = status_code
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))

    def send_error_response(self, status_code: int, code: str, message: str) -> None:
        """发送错误响应"""
        self.send_json_response(status_code, {
            "success": False,
            "error": {
                "code": code,
                "message": message
            }
        })

    @log_request
    @handle_errors
    def do_GET(self):
        """处理 GET 请求"""
        self._route_request()

    @log_request
    @handle_errors
    def do_POST(self):
        """处理 POST 请求"""
        self._route_request()

    @log_request
    @handle_errors
    def do_PUT(self):
        """处理 PUT 请求"""
        self._route_request()

    @log_request
    @handle_errors
    def do_PATCH(self):
        """处理 PATCH 请求"""
        self._route_request()

    @log_request
    @handle_errors
    def do_DELETE(self):
        """处理 DELETE 请求"""
        self._route_request()

    @log_request
    @handle_errors
    def do_OPTIONS(self):
        """处理 OPTIONS 请求（CORS 预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def _route_request(self):
        """路由请求到对应的处理器"""
        path = self.path.split('?')[0]

        # 定义路由
        self._setup_routes()

        # 查找匹配的路由
        result = router.route(self.command, self.path)

        if result is None:
            self.send_error_response(404, "NOT_FOUND", "接口不存在")
            return

        handler_func, params = result
        result_data = handler_func()

        if result_data is not None:
            status_code = 200
            if self.command == 'POST' and 'data' in result_data and 'message' in result_data:
                status_code = 201  # Created
            elif self.command == 'DELETE':
                status_code = 200
            self.send_json_response(status_code, {"success": True, **result_data})

    def _setup_routes(self):
        """设置路由"""
        # 清除旧路由（避免重复添加）
        router.routes.clear()

        # 认证路由
        @router.post('/api/auth/register')
        def register():
            return AuthHandler(self).register()

        @router.post('/api/auth/login')
        def login():
            return AuthHandler(self).login()

        # 书籍路由
        @router.get('/api/books')
        def list_books():
            return BookHandler(self).list_books()

        @router.post('/api/books')
        def create_book():
            return BookHandler(self).create_book()

        @router.get('/api/books/([0-9]+)')
        def get_book(book_id: str):
            return BookHandler(self).get_book(int(book_id))

        @router.put('/api/books/([0-9]+)')
        def update_book(book_id: str):
            return BookHandler(self).update_book(int(book_id))

        @router.patch('/api/books/([0-9]+)')
        def patch_book(book_id: str):
            return BookHandler(self).patch_book(int(book_id))

        @router.delete('/api/books/([0-9]+)')
        def delete_book(book_id: str):
            return BookHandler(self).delete_book(int(book_id))

        # 用户路由
        @router.get('/api/users/profile')
        def get_profile():
            return UserHandler(self).get_profile()

        @router.put('/api/users/profile')
        def update_profile():
            return UserHandler(self).update_profile()


def create_server() -> HTTPServer:
    """创建 HTTP 服务器"""
    # 初始化数据库
    db.connect()
    logger.info(f"数据库已初始化：{Config.DATABASE_PATH}")

    server = HTTPServer((Config.HOST, Config.PORT), APIHandler)
    logger.info(f"服务器启动：http://{Config.HOST}:{Config.PORT}")
    return server


def run_server():
    """运行服务器"""
    server = create_server()
    print(f"\n服务器运行在 http://{Config.HOST}:{Config.PORT}")
    print("按 Ctrl+C 停止服务器\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("服务器停止中...")
        server.shutdown()
        db.close()
        logger.info("服务器已停止")


if __name__ == '__main__':
    run_server()
