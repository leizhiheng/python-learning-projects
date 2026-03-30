"""用户相关处理器"""
import json
from http.server import BaseHTTPRequestHandler
from models.user import UserRepository
from utils.validators import (
    validate_required, validate_username, validate_password,
    validate_email, ValidationError
)
from middleware.auth import require_auth
from middleware.error_handler import BadRequestError, ConflictError


class UserHandler:
    """用户处理器"""

    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    @require_auth
    def get_profile(self) -> dict:
        """获取当前用户信息"""
        user_id = self.handler.current_user['user_id']
        user = UserRepository.get_by_id(user_id)

        if not user:
            return {'error': '用户不存在'}

        return {'data': user.to_dict()}

    @require_auth
    def update_profile(self) -> dict:
        """更新当前用户信息"""
        content_length = int(self.handler.headers.get('Content-Length', 0))
        body = self.handler.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise BadRequestError("无效的 JSON 格式")

        user_id = self.handler.current_user['user_id']

        # 验证字段
        if 'username' in data:
            validate_username(data['username'])
        if 'email' in data:
            if not validate_email(data['email']):
                raise BadRequestError("邮箱格式不正确")

        updated = UserRepository.update(user_id, **data)

        if not updated:
            raise ConflictError("更新失败，用户名或邮箱可能已存在")

        return {
            'data': updated.to_dict(),
            'message': '更新成功'
        }
