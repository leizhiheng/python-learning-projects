"""参数验证工具"""
import re
from typing import Optional, Tuple, Any, Dict


class ValidationError(Exception):
    """验证异常"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_required(data: Dict[str, Any], *fields: str) -> None:
    """验证必填字段"""
    for field in fields:
        if field not in data or data[field] is None:
            raise ValidationError(field, f"{field} 是必填项")
        if isinstance(data[field], str) and not data[field].strip():
            raise ValidationError(field, f"{field} 不能为空字符串")


def validate_string_length(value: str, min_len: int = 0, max_len: int = 1000,
                           field_name: str = "字段") -> None:
    """验证字符串长度"""
    if len(value) < min_len:
        raise ValidationError(field_name, f"{field_name} 至少需要{min_len}个字符")
    if len(value) > max_len:
        raise ValidationError(field_name, f"{field_name} 不能超过{max_len}个字符")


def validate_number_range(value: float, min_val: Optional[float] = None,
                          max_val: Optional[float] = None,
                          field_name: str = "数值") -> None:
    """验证数值范围"""
    if min_val is not None and value < min_val:
        raise ValidationError(field_name, f"{field_name} 不能小于{min_val}")
    if max_val is not None and value > max_val:
        raise ValidationError(field_name, f"{field_name} 不能大于{max_val}")


def validate_username(username: str) -> None:
    """验证用户名格式"""
    validate_string_length(username, 3, 32, "用户名")
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("username", "用户名只能包含字母、数字和下划线")


def validate_password(password: str) -> None:
    """验证密码强度"""
    validate_string_length(password, 6, 128, "密码")


def parse_int(value: Any, default: int = 0) -> int:
    """安全地解析整数"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_float(value: Any, default: float = 0.0) -> float:
    """安全地解析浮点数"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_pagination(query: Dict[str, Any]) -> Tuple[int, int]:
    """解析分页参数"""
    page = max(1, parse_int(query.get('page', 1)))
    limit = parse_int(query.get('limit', 10))
    limit = max(1, min(limit, 100))  # 限制 1-100
    return page, limit
