import argparse
import sys
from datetime import datetime
from typing import List, Optional

from models import Task, Priority, Status
from storage import Storage

class TodoCli:
    def __init__(self):
        self.storage = Storage()

    def add_task(self, title: str, description: Optional[str] = None,
                 priority: str = "medium", due: Optional[str] = None) -> None:
        """添加新任务"""
        try:
            priority_enum = Priority(priority.lower())
        except:
            print(f"错误：无效优先级 '{priority}', 可选值： low, medium, high")
            return
        
        due_date = None
        if due:
            try:
                due_date = datetime.strftime(due, "%Y-%m-%d")
            except:
                print(f"错误：无效的日期格式 '{due}', 请使用 YYYY-MM-DD 格式")
                return
        
        task = Task(
            id = 0,
            title = title,
            description = description,
            priority = priority_enum,
            due_date = due_date,
        )

        added = self.storage.add_task(task=task)
        print(f"[OK] 任务已添加： #{added.id} - {added.title}")


# 实现命令行解析
def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="命令行待办事项管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        示例：
        %(prog)s add "买牛奶" --priority high --due 2026-03-31
        %(prog)s list --status pending
        %(prog)s done 1 2 3
        %(prog)s edit 1 --title "新标题"
        %(prog)s delete 1
        """
    )

    # 创建子命令容器
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # add 命令
    # 添加子任务的名称和简单描述
    add_parser = subparsers.add_parser('add', help='添加新任务')
    # 添加参数和参数描述，第一个未知参数是参数名称，后面的kwarg是参数说明，
    add_parser.add_argument('title', help='任务描述')
    # 添加可选参数，可选参数使用--开头。dest参数是目的吧。
    add_parser.add_argument('--desc', dest='description', help='任务描述')
    # 添加可选参数，并且是枚举类型的参数，枚举值使用choices列表列表，default：设置默认值
    add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium', help='优先级(默认：medium)')
    add_parser.add_argument('--due', help='截止日期（YYYY-MM-DD')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--status', choices=['pending', 'done'], help='按状态过滤')
    list_parser.add_argument('--priority', choices=['low', 'medium', 'high'], help='按优先级过滤')

    # done 命令
    done_parser = subparsers.add_parser('done', help='完成任务')
    # 通过type设置参数类型。nargs='+'表示1个或多个参数，并将它们存储为列表。也可是0或多个(*)，可以使是0或一个(?)
    done_parser.add_argument('ids', type=int, nargs='+', help='任务 ID 列表')

    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除任务')
    delete_parser.add_argument('id', type=int, help='任务ID')

    # edit命令
    edit_parser = subparsers.add_parser('edit', help='编辑任务')
    edit_parser.add_argument('id', type=int, help='任务ID')
    edit_parser.add_argument('--title', help='新标题')
    edit_parser.add_argument('--desc', '--description', dest='description', help='新描述')
    edit_parser.add_argument('--priority', choices=['low', 'medium', 'high'], help='新优先级')
    edit_parser.add_argument('--due', help='新截止日期(YYYY-MM-DD)')

    # show 命令
    show_parser = subparsers.add_parser('show')
    show_parser.add_argument('id', type=int, help='任务 ID')

    return parser


    
def main():
    print("待办事项列表启动！")
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cli = TodoCli()

    if args.command == 'add':
        cli.add_task(args.title, args.description, args.priority, args.due)


# 定义入口函数
if __name__ == "__main__":
    main()