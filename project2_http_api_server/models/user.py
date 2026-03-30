"""用户数据模型"""
import sqlite3
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from utils.db import get_db
from utils.jwt import hash_password


@dataclass
class User:
    """用户模型"""
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self, include_email: bool = True) -> Dict[str, Any]:
        """转换为字典"""
        data = {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_email:
            data['email'] = self.email
        return data

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'User':
        """从数据库行创建实例"""
        return cls(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
        )


class UserRepository:
    """用户数据访问层"""

    @staticmethod
    def create(username: str, email: str, password: str) -> Optional[User]:
        """创建新用户"""
        db = get_db()
        password_hash = hash_password(password)

        try:
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO users (username, email, password_hash)
                   VALUES (?, ?, ?)''',
                (username, email, password_hash)
            )
            db.commit()
            user_id = cursor.lastrowid
            cursor.close()

            return User(
                id=user_id,
                username=username,
                email=email,
                password_hash=password_hash
            )
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return User.from_row(row)
        return None

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return User.from_row(row)
        return None

    @staticmethod
    def update(user_id: int, **kwargs) -> Optional[User]:
        """更新用户信息"""
        db = get_db()

        allowed_fields = {'username', 'email'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return None

        set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [user_id]

        try:
            cursor = db.cursor()
            cursor.execute(
                f'UPDATE users SET {set_clause} WHERE id = ?',
                values
            )
            db.commit()
            cursor.close()

            if cursor.rowcount > 0:
                return User.get_by_id(user_id)
            return None
        except sqlite3.IntegrityError:
            return None
