"""书籍相关处理器"""
import json
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any, Optional, Tuple
from models.book import Book, BookRepository
from utils.validators import (
    validate_required, validate_number_range, ValidationError,
    parse_int, parse_float, parse_pagination
)
from middleware.error_handler import (
    BadRequestError, NotFoundError, ForbiddenError
)
from middleware.auth import require_auth


class BookHandler:
    """书籍处理器"""

    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def _parse_query(self, query_string: str) -> Dict[str, str]:
        """解析查询参数"""
        params = {}
        if not query_string:
            return params

        for part in query_string.split('&'):
            if '=' in part:
                key, value = part.split('=', 1)
                params[key] = value
            else:
                params[part] = ''
        return params

    def list_books(self) -> Dict[str, Any]:
        """获取书籍列表（支持分页、过滤、搜索）"""
        # 解析 URL
        path_parts = self.handler.path.split('?')
        query_string = path_parts[1] if len(path_parts) > 1 else ''
        query = self._parse_query(query_string)

        # 解析分页
        page, limit = parse_pagination(query)
        offset = (page - 1) * limit

        # 构建过滤条件
        where_parts = []
        params = []

        # 搜索
        search_query = query.get('q', '').strip()
        if search_query:
            # 搜索单独处理
            books = BookRepository.search(search_query)
            return {
                'data': [b.to_dict() for b in books],
                'pagination': {
                    'page': 1,
                    'limit': len(books),
                    'total': len(books),
                    'total_pages': 1
                }
            }

        # 作者过滤
        author = query.get('author', '').strip()
        if author:
            where_parts.append('author = ?')
            params.append(author)

        # 分类过滤
        category = query.get('category', '').strip()
        if category:
            where_parts.append('category = ?')
            params.append(category)

        # 价格范围
        min_price = query.get('min_price', '').strip()
        if min_price:
            where_parts.append('price >= ?')
            params.append(parse_float(min_price))

        max_price = query.get('max_price', '').strip()
        if max_price:
            where_parts.append('price <= ?')
            params.append(parse_float(max_price))

        # 排序
        sort_by = query.get('sort', 'created_at')
        order = query.get('order', 'DESC').upper()
        if sort_by not in ['title', 'author', 'price', 'stock', 'created_at']:
            sort_by = 'created_at'
        if order not in ['ASC', 'DESC']:
            order = 'DESC'

        where_clause = ' AND '.join(where_parts) if where_parts else ''

        # 获取数据
        books, total = BookRepository.get_all(
            where_clause=where_clause,
            params=tuple(params),
            order_by=sort_by,
            order=order,
            offset=offset,
            limit=limit
        )

        total_pages = (total + limit - 1) // limit

        return {
            'data': [b.to_dict() for b in books],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': total_pages
            }
        }

    @require_auth
    def create_book(self) -> Dict[str, Any]:
        """创建新书籍"""
        content_length = int(self.handler.headers.get('Content-Length', 0))
        body = self.handler.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise BadRequestError("无效的 JSON 格式")

        validate_required(data, 'title', 'author')

        # 验证数值
        if 'price' in data and data['price'] is not None:
            validate_number_range(data['price'], 0, field_name='price')
        if 'stock' in data and data['stock'] is not None:
            validate_number_range(data['stock'], 0, field_name='stock')

        book = BookRepository.create(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            price=data.get('price'),
            stock=data.get('stock', 0),
            category=data.get('category'),
            description=data.get('description'),
            owner_id=self.handler.current_user['user_id']
        )

        if not book:
            raise BadRequestError("创建失败，ISBN 可能已存在")

        return {
            'data': book.to_dict(),
            'message': '创建成功'
        }

    def get_book(self, book_id: int) -> Dict[str, Any]:
        """获取单本书籍详情"""
        book = BookRepository.get_by_id(book_id)
        if not book:
            raise NotFoundError("书籍不存在")

        return {'data': book.to_dict()}

    @require_auth
    def update_book(self, book_id: int) -> Dict[str, Any]:
        """更新书籍（全量更新）"""
        book = BookRepository.get_by_id(book_id)
        if not book:
            raise NotFoundError("书籍不存在")

        # 检查权限
        if book.owner_id != self.handler.current_user['user_id']:
            raise ForbiddenError("无权修改此书籍")

        content_length = int(self.handler.headers.get('Content-Length', 0))
        body = self.handler.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise BadRequestError("无效的 JSON 格式")

        validate_required(data, 'title', 'author')

        if 'price' in data and data['price'] is not None:
            validate_number_range(data['price'], 0, field_name='price')
        if 'stock' in data and data['stock'] is not None:
            validate_number_range(data['stock'], 0, field_name='stock')

        updated = BookRepository.update(book_id, **data)
        if not updated:
            raise BadRequestError("更新失败")

        return {
            'data': updated.to_dict(),
            'message': '更新成功'
        }

    @require_auth
    def patch_book(self, book_id: int) -> Dict[str, Any]:
        """部分更新书籍"""
        book = BookRepository.get_by_id(book_id)
        if not book:
            raise NotFoundError("书籍不存在")

        # 检查权限
        if book.owner_id != self.handler.current_user['user_id']:
            raise ForbiddenError("无权修改此书籍")

        content_length = int(self.handler.headers.get('Content-Length', 0))
        body = self.handler.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise BadRequestError("无效的 JSON 格式")

        if 'price' in data and data['price'] is not None:
            validate_number_range(data['price'], 0, field_name='price')
        if 'stock' in data and data['stock'] is not None:
            validate_number_range(data['stock'], 0, field_name='stock')

        updated = BookRepository.update(book_id, **data)
        if not updated:
            raise BadRequestError("更新失败")

        return {
            'data': updated.to_dict(),
            'message': '更新成功'
        }

    @require_auth
    def delete_book(self, book_id: int) -> Dict[str, Any]:
        """删除书籍"""
        book = BookRepository.get_by_id(book_id)
        if not book:
            raise NotFoundError("书籍不存在")

        # 检查权限
        if book.owner_id != self.handler.current_user['user_id']:
            raise ForbiddenError("无权删除此书籍")

        if not BookRepository.delete(book_id):
            raise BadRequestError("删除失败")

        return {'message': '删除成功'}
