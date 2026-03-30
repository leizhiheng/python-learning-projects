#!/usr/bin/env python3
"""
书籍管理 API 服务器 - 主入口

Usage:
    python app.py runserver    # 启动服务器
    python app.py init         # 初始化数据库
"""

import sys
import argparse

from server import run_server
from utils.db import db
from utils.jwt import hash_password
from models.user import UserRepository
from models.book import BookRepository


def init_db():
    """初始化数据库并添加测试数据"""
    db.connect()
    print("数据库已初始化")

    # 创建测试用户
    user = UserRepository.get_by_username('admin')
    if not user:
        user = UserRepository.create('admin', 'admin@example.com', 'admin123')
        if user:
            print(f"创建测试用户：admin (密码：admin123)")

    # 创建测试书籍
    if BookRepository.get_by_id(1) is None:
        test_books = [
            {'title': 'Python 编程：从入门到实践', 'author': 'Eric Matthes', 'isbn': '978-7-115-42802-8', 'price': 89.0, 'stock': 10, 'category': '编程', 'description': 'Python 入门经典图书'},
            {'title': '流畅的 Python', 'author': 'Luciano Ramalho', 'isbn': '978-7-115-45466-9', 'price': 129.0, 'stock': 5, 'category': '编程', 'description': 'Python 进阶必读'},
            {'title': '算法导论', 'author': 'Thomas H. Cormen', 'isbn': '978-7-111-40701-0', 'price': 128.0, 'stock': 3, 'category': '计算机', 'description': '算法经典教材'},
            {'title': '设计模式：可复用面向对象软件的基础', 'author': 'Erich Gamma', 'isbn': '978-7-111-07575-2', 'price': 79.0, 'stock': 8, 'category': '编程', 'description': '设计模式经典著作'},
            {'title': '代码整洁之道', 'author': 'Robert C. Martin', 'isbn': '978-7-115-21750-9', 'price': 69.0, 'stock': 15, 'category': '编程', 'description': '编写高质量代码的指南'},
        ]

        for book_data in test_books:
            BookRepository.create(**book_data)

        print(f"创建 {len(test_books)} 本测试书籍")

    print("\n测试数据已准备就绪")
    print("API 端点:")
    print("  POST /api/auth/register - 用户注册")
    print("  POST /api/auth/login    - 用户登录")
    print("  GET  /api/books         - 获取书籍列表")
    print("  POST /api/books         - 创建书籍 (需认证)")
    print("  GET  /api/books/{id}    - 获取书籍详情")
    print("  PUT  /api/books/{id}    - 更新书籍 (需认证)")
    print("  DELETE /api/books/{id}  - 删除书籍 (需认证)")


def main():
    parser = argparse.ArgumentParser(description='书籍管理 API 服务器')
    parser.add_argument('command', choices=['runserver', 'init'],
                       help='runserver: 启动服务器，init: 初始化数据库')

    args = parser.parse_args()

    if args.command == 'runserver':
        run_server()
    elif args.command == 'init':
        init_db()


if __name__ == '__main__':
    main()
