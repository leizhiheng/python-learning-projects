"""认证相关处理器"""
import json
from http.server import BaseHTTPRequestHandler
from models.user import UserRepository
from utils.jwt import create_token, verify_password, hash_password
from utils.validators import (
    validate_required, validate_username, validate_password,
    validate_email, ValidationError
)
from middleware.error_handler import BadRequestError, ConflictError, UnauthorizedError


class AuthHandler:
    """认证处理器"""

    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def register(self) -> dict:
        """用户注册"""
        content_length = int(self.handler.headers.get('Content-Length', 0))
        body = self.handler.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise BadRequestError("无效的 JSON 格式")

        # 验证必填字段
        validate_required(data, 'username', 'email', 'password')
        validate_username(data['username'])
        validate_password(data['password'])

        if not validate_email(data['email']):
            raise BadRequestError("邮箱格式不正确")

        # 创建用户
        user = UserRepository.create(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise ConflictError("用户名或邮箱已存在")

        return {
            'user': user.to_dict(),
            'message': '注册成功'
        }

    def login(self) -> dict:
        """用户登录"""
        content_length = int(self.handler.headers.get('Content-Length', 0))
        body = self.handler.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise BadRequestError("无效的 JSON 格式")

        validate_required(data, 'username', 'password')

        # 查找用户
        user = UserRepository.get_by_username(data['username'])
        if not user:
            raise UnauthorizedError("用户名或密码错误")

        # 验证密码
        if not verify_password(data['password'], user.password_hash):
            raise UnauthorizedError("用户名或密码错误")

        # 生成 token
        token = create_token(user.id, user.username)

        return {
            'token': token,
            'user': user.to_dict(),
            'message': '登录成功'
        }
