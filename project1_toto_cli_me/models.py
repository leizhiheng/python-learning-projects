"""数据模型定义"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(Enum):
    PENDING = "pending"
    DONE = "done"

@dataclass
class Task:
    """待办任务数据模型"""
    id: int
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """转换为字典格式，用户JSON序列化"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """从字典里创建任务实例。这是一个类方法"""
        return cls(
            id = data['id'],
            title = data['title'],
            description = data.get('description'),
            priority = Priority(data.get('priority', 'medium')),
            status = Status(data.get('status', 'pending')),
            created_at = datetime.fromisoformat(data['created_at']),
            due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            completed_at = datetime.fromisoformat(data['completed_at']) if (data.get('completed_at')) else None
        )
    
    def isOverDue(self) -> bool:
        """检查任务是否过期"""
        if self.due_date and self.status == Status.PENDING:
            return datetime.now() > self.due_date
        return False

    def __str__(self) -> str:
        """任务的字符串表示，相当于 Java 的 toString()"""
        status_icon = '√' if self.status == Status.DONE else '□'
        priority_icon = {
            Priority.LOW: "○",
            Priority.MEDIUM: "●",
            Priority.HIGH: "△"
        }[self.priority]
        overdue_marker = " [过期]" if self.isOverDue() else ""
        return f"[{status_icon}] {self.id}. {self.title} {priority_icon}{overdue_marker}"

