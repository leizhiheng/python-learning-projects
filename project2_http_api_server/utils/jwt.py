"""JWT 工具模块"""
import hashlib
import hmac
import time
import json
import base64
from typing import Optional, Dict, Any
from config import Config


def _base64url_encode(data: bytes) -> str:
    """Base64 URL 安全编码"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def _base64url_decode(data: str) -> bytes:
    """Base64 URL 安全解码"""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)


def _create_hash(payload: str, secret: str) -> str:
    """创建 HMAC-SHA256 哈希"""
    return hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).digest()


def create_token(user_id: int, username: str) -> str:
    """创建 JWT token"""
    header = {
        'alg': 'HS256',
        'typ': 'JWT'
    }

    now = int(time.time())
    payload = {
        'user_id': user_id,
        'username': username,
        'iat': now,
        'exp': now + Config.JWT_EXPIRY_HOURS * 3600
    }

    header_b64 = _base64url_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = _base64url_encode(json.dumps(payload).encode('utf-8'))

    signature = _create_hash(f"{header_b64}.{payload_b64}", Config.JWT_SECRET)
    signature_b64 = _base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """验证并解码 JWT token"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts

        # 验证签名
        expected_signature = _create_hash(
            f"{header_b64}.{payload_b64}",
            Config.JWT_SECRET
        )
        actual_signature = _base64url_decode(signature_b64)

        if not hmac.compare_digest(expected_signature, actual_signature):
            return None

        # 解码 payload
        payload = json.loads(_base64url_decode(payload_b64))

        # 检查过期时间
        if 'exp' in payload and time.time() > payload['exp']:
            return None

        return payload

    except (json.JSONDecodeError, ValueError, KeyError):
        return None


def hash_password(password: str) -> str:
    """密码哈希"""
    salt = "python_books_api_salt_v1"
    return hashlib.sha256(f"{password}{salt}".encode('utf-8')).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """验证密码"""
    return hash_password(password) == password_hash
