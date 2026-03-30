"""书籍数据模型"""
import sqlite3
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from utils.db import get_db


@dataclass
class Book:
    """书籍模型"""
    id: int
    title: str
    author: str
    isbn: Optional[str] = None
    price: Optional[float] = None
    stock: int = 0
    category: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    owner_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'owner_id': self.owner_id,
        }

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Book':
        """从数据库行创建实例"""
        return cls(
            id=row['id'],
            title=row['title'],
            author=row['author'],
            isbn=row['isbn'],
            price=row['price'],
            stock=row['stock'],
            category=row['category'],
            description=row['description'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
            owner_id=row['owner_id'],
        )


class BookRepository:
    """书籍数据访问层"""

    @staticmethod
    def create(title: str, author: str, isbn: Optional[str] = None,
               price: Optional[float] = None, stock: int = 0,
               category: Optional[str] = None, description: Optional[str] = None,
               owner_id: Optional[int] = None) -> Optional[Book]:
        """创建新书籍"""
        db = get_db()

        try:
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO books (title, author, isbn, price, stock, category, description, owner_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (title, author, isbn, price, stock, category, description, owner_id)
            )
            db.commit()
            book_id = cursor.lastrowid
            cursor.close()

            return Book.get_by_id(book_id)
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_by_id(book_id: int) -> Optional[Book]:
        """根据 ID 获取书籍"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return Book.from_row(row)
        return None

    @staticmethod
    def get_all(where_clause: str = "", params: Tuple = (),
                order_by: str = "created_at", order: str = "DESC",
                offset: int = 0, limit: int = 10) -> Tuple[List[Book], int]:
        """获取书籍列表（带分页和过滤）"""
        db = get_db()
        cursor = db.cursor()

        # 获取总数
        count_sql = 'SELECT COUNT(*) FROM books'
        if where_clause:
            count_sql += f' WHERE {where_clause}'
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        # 获取数据
        sql = 'SELECT * FROM books'
        if where_clause:
            sql += f' WHERE {where_clause}'
        sql += f' ORDER BY {order_by} {order} LIMIT ? OFFSET ?'

        cursor.execute(sql, params + (limit, offset))
        rows = cursor.fetchall()
        cursor.close()

        books = [Book.from_row(row) for row in rows]
        return books, total

    @staticmethod
    def update(book_id: int, **kwargs) -> Optional[Book]:
        """更新书籍信息"""
        db = get_db()

        allowed_fields = {'title', 'author', 'isbn', 'price', 'stock',
                         'category', 'description'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return None

        set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [book_id]

        try:
            cursor = db.cursor()
            cursor.execute(
                f'UPDATE books SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                values
            )
            db.commit()
            cursor.close()

            if cursor.rowcount > 0:
                return BookRepository.get_by_id(book_id)
            return None
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def delete(book_id: int) -> bool:
        """删除书籍"""
        db = get_db()
        try:
            cursor = db.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            db.commit()
            result = cursor.rowcount > 0
            cursor.close()
            return result
        except sqlite3.Error:
            return False

    @staticmethod
    def search(query: str) -> List[Book]:
        """搜索书籍"""
        db = get_db()
        cursor = db.cursor()
        search_pattern = f'%{query}%'
        cursor.execute(
            '''SELECT * FROM books
               WHERE title LIKE ? OR author LIKE ? OR description LIKE ?
               ORDER BY created_at DESC''',
            (search_pattern, search_pattern, search_pattern)
        )
        rows = cursor.fetchall()
        cursor.close()
        return [Book.from_row(row) for row in rows]
