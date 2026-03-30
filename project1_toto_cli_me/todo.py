import argparse

# 实现命令行解析
def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="命令行待办事项管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        示例：
        %(prop)s add "买牛奶" --priority high --due 2026-03-31
        %(prog)s list --status pending
        %(prog)s done 1 2 3
        %(prog)s edit 1 --title "新标题"
        %(prog)s delete 1
        """
    )

    # 创建子命令容器
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 添加子任务的名称和简单描述
    add_parser = subparsers.add_parser('add', help='添加新任务')
    # 添加参数和参数描述，第一个未知参数是参数名称，后面的kwarg是参数说明，
    add_parser.add_argument('title', help='任务描述')
    # 添加可选参数，可选参数使用--开头。dest参数是目的吧。
    add_parser.add_argument('--desc', dest='description', help='任务描述')
    # 添加可选参数，并且是枚举类型的参数，枚举值使用choices列表列表，default：设置默认值
    add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium', help='优先级(默认：medium)')
    add_parser.add_argument('--due', help='截止日期（YYYY-MM-DD')


def main():
    print("待办事项列表启动！")

# 定义入口函数
if __name__ == "__main__":
    main()