import json
from pathlib import Path
from typing import List, Optional
from models import Task

class Storage:
    """任务数据存储类"""
    def __init__(self, data_file: str = "data.json") -> None:
        self.data_file = Path(data_file)
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self._load()
        

    def _load(self) -> None:
        """从文件加载任务数据"""
        if not self.data_file.exists():
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data.get('tasks', [])]
                self.next_id = data.get('next_id', 1)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"告警：数据文件加载失败 {e}")
            self.tasks = []
            self.next_id = 1
    
    def _save(self) -> bool:
        """保存任务数据到文件"""
        try:
            data = {
                'tasks': [t.to_dict() for t in self.tasks],
                'next_id': self.next_id,
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"错误：保存数据失败 - {e}")
            return False
    
    def add_task(self, task: Task) -> Task:
        """添加新任务"""
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self._save()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """根据 ID 获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        return self.tasks
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """根据状态过滤任务"""
        return [t for t in self.tasks if t.status.value == status]
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """根据优先级过滤任务"""
        return [t for t in self.tasks if t.priority.value == priority]
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """更新任务"""
        task = self.get_task(task_id=task_id)
        if not task:
            return None
        
        for key, value in kwargs.items():
            # hasattr 判断对象中是否含有某个key
            if hasattr(task, key):
                # 更新对象中的某个key
                setattr(task, key, value)

        # 保存任务列表
        self._save()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """删除任务"""
        task = self.get_task(task_id=task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self._save()
        return True
    
    def get_next_id(self) -> int:
        return self.next_id