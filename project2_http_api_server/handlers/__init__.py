"""Handler 模块初始化"""
from .auth_handler import AuthHandler
from .book_handler import BookHandler
from .user_handler import UserHandler

__all__ = [
    'AuthHandler',
    'BookHandler',
    'UserHandler',
]
