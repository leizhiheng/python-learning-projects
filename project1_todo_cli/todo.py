#!/usr/bin/env python3
"""
命令行待办事项管理器
Usage:
    python todo.py add "任务标题" --priority high --due 2024-01-15
    python todo.py list [--status pending/done] [--priority low/medium/high]
    python todo.py done <id> [id...]
    python todo.py delete <id>
    python todo.py edit <id> [--title "新标题"] [--priority low/medium/high]
    python todo.py show <id>
"""

import argparse
import sys
from datetime import datetime
from typing import List, Optional

from models import Task, Priority, Status
from storage import Storage


class TodoCLI:
    """待办事项命令行界面"""

    def __init__(self):
        self.storage = Storage()

    def add_task(self, title: str, description: Optional[str] = None,
                 priority: str = "medium", due: Optional[str] = None) -> None:
        """添加新任务"""
        try:
            priority_enum = Priority(priority.lower())
        except ValueError:
            print(f"错误：无效的优先级 '{priority}'，可选值：low, medium, high")
            return

        due_date = None
        if due:
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                print(f"错误：无效的日期格式 '{due}'，请使用 YYYY-MM-DD 格式")
                return

        task = Task(
            id=0,
            title=title,
            description=description,
            priority=priority_enum,
            due_date=due_date
        )

        added = self.storage.add_task(task)
        print(f"[OK] 任务已添加：#{added.id} - {added.title}")

    def list_tasks(self, status: Optional[str] = None,
                   priority: Optional[str] = None) -> None:
        """列出任务"""
        tasks = self.storage.get_all_tasks()

        # 过滤
        if status:
            tasks = self.storage.get_tasks_by_status(status)
        if priority:
            tasks = self.storage.get_tasks_by_priority(priority)

        if not tasks:
            print("没有找到任务")
            return

        # 打印表头
        print(f"\n{'ID':<5} {'状态':<3} {'优先级':<6} {'标题':<25} {'截止日期':<12}")
        print("-" * 60)

        # 排序：未完成在前，高优先级在前
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        tasks = sorted(tasks, key=lambda t: (t.status.value, -priority_order[t.priority]))

        for task in tasks:
            status_icon = "✓" if task.status == Status.DONE else "□"
            priority_str = task.priority.value[:4]
            due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "-"

            if task.is_overdue():
                due_str += " (过期)"

            # 截断长标题
            title = task.title[:22] + "..." if len(task.title) > 25 else task.title

            print(f"{task.id:<5} {status_icon:<3} {priority_str:<6} {title:<25} {due_str:<12}")

        print(f"\n共 {len(tasks)} 个任务")

    def complete_task(self, task_ids: List[int]) -> None:
        """完成任务"""
        success_count = 0
        for task_id in task_ids:
            task = self.storage.get_task(task_id)
            if not task:
                print(f"错误：任务 #{task_id} 不存在")
                continue

            if task.status == Status.DONE:
                print(f"任务 #{task_id} 已经完成过了")
                continue

            self.storage.update_task(task_id, status=Status.DONE, completed_at=datetime.now())
            print(f"[OK] 任务 #{task_id} 已完成：{task.title}")
            success_count += 1

        if success_count:
            print(f"共完成 {success_count} 个任务")

    def delete_task(self, task_id: int) -> None:
        """删除任务"""
        task = self.storage.get_task(task_id)
        if not task:
            print(f"错误：任务 #{task_id} 不存在")
            return

        confirm = input(f"确认删除任务 #{task_id} '{task.title}'? (y/N): ")
        if confirm.lower() != 'y':
            print("已取消删除")
            return

        if self.storage.delete_task(task_id):
            print(f"[OK] 任务已删除：#{task_id}")
        else:
            print("删除失败")

    def edit_task(self, task_id: int, title: Optional[str] = None,
                  description: Optional[str] = None,
                  priority: Optional[str] = None,
                  due: Optional[str] = None) -> None:
        """编辑任务"""
        task = self.storage.get_task(task_id)
        if not task:
            print(f"错误：任务 #{task_id} 不存在")
            return

        updates = {}
        if title is not None:
            updates['title'] = title
        if description is not None:
            updates['description'] = description
        if priority is not None:
            try:
                updates['priority'] = Priority(priority.lower())
            except ValueError:
                print(f"错误：无效的优先级 '{priority}'")
                return
        if due is not None:
            if due == "":
                updates['due_date'] = None
            else:
                try:
                    updates['due_date'] = datetime.strptime(due, "%Y-%m-%d")
                except ValueError:
                    print(f"错误：无效的日期格式 '{due}'")
                    return

        if not updates:
            print("没有提供任何要修改的内容")
            return

        updated = self.storage.update_task(task_id, **updates)
        if updated:
            print(f"[OK] 任务已更新：#{task_id}")
            self.show_task(task_id)

    def show_task(self, task_id: int) -> None:
        """显示任务详情"""
        task = self.storage.get_task(task_id)
        if not task:
            print(f"错误：任务 #{task_id} 不存在")
            return

        print("\n" + "=" * 40)
        print(f"任务 #{task.id}")
        print("=" * 40)
        print(f"标题：{task.title}")
        print(f"描述：{task.description or '无'}")
        print(f"状态：{'已完成 ✓' if task.status == Status.DONE else '待办 □'}")
        print(f"优先级：{task.priority.value}")

        if task.due_date:
            print(f"截止日期：{task.due_date.strftime('%Y-%m-%d %H:%M')}")
            if task.is_overdue():
                print("  ⚠ 已过期!")

        print(f"创建时间：{task.created_at.strftime('%Y-%m-%d %H:%M')}")

        if task.completed_at:
            print(f"完成时间：{task.completed_at.strftime('%Y-%m-%d %H:%M')}")

        print("=" * 40)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="命令行待办事项管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s add "买牛奶" --priority high --due 2024-01-15
  %(prog)s list --status pending
  %(prog)s done 1 2 3
  %(prog)s edit 1 --title "新标题"
  %(prog)s delete 1
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # add 命令
    add_parser = subparsers.add_parser('add', help='添加新任务')
    add_parser.add_argument('title', help='任务标题')
    add_parser.add_argument('--desc', '--description', dest='description',
                           help='任务描述')
    add_parser.add_argument('--priority', choices=['low', 'medium', 'high'],
                           default='medium', help='优先级 (默认：medium)')
    add_parser.add_argument('--due', help='截止日期 (YYYY-MM-DD)')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--status', choices=['pending', 'done'],
                            help='按状态过滤')
    list_parser.add_argument('--priority', choices=['low', 'medium', 'high'],
                            help='按优先级过滤')

    # done 命令
    done_parser = subparsers.add_parser('done', help='完成任务')
    done_parser.add_argument('ids', type=int, nargs='+',
                            help='任务 ID 列表')

    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除任务')
    delete_parser.add_argument('id', type=int, help='任务 ID')

    # edit 命令
    edit_parser = subparsers.add_parser('edit', help='编辑任务')
    edit_parser.add_argument('id', type=int, help='任务 ID')
    edit_parser.add_argument('--title', help='新标题')
    edit_parser.add_argument('--desc', '--description', dest='description',
                            help='新描述')
    edit_parser.add_argument('--priority', choices=['low', 'medium', 'high'],
                            help='新优先级')
    edit_parser.add_argument('--due', help='新截止日期 (YYYY-MM-DD)')

    # show 命令
    show_parser = subparsers.add_parser('show', help='显示任务详情')
    show_parser.add_argument('id', type=int, help='任务 ID')

    return parser


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cli = TodoCLI()

    if args.command == 'add':
        cli.add_task(args.title, args.description, args.priority, args.due)
    elif args.command == 'list':
        cli.list_tasks(args.status, args.priority)
    elif args.command == 'done':
        cli.complete_task(args.ids)
    elif args.command == 'delete':
        cli.delete_task(args.id)
    elif args.command == 'edit':
        cli.edit_task(args.id, args.title, args.description,
                     args.priority, args.due)
    elif args.command == 'show':
        cli.show_task(args.id)


if __name__ == '__main__':
    main()
