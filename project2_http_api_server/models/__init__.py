"""模型模块初始化"""
from .user import User, UserRepository
from .book import Book, BookRepository

__all__ = [
    'User',
    'UserRepository',
    'Book',
    'BookRepository',
]
