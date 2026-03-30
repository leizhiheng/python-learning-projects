# 项目一：命令行待办事项管理器 (Todo CLI)

## 项目概述
构建一个功能完整的命令行待办事项管理应用，使用文件存储数据。

## 技术要求
- 使用 `argparse` 模块处理命令行参数
- 使用 `json` 模块进行数据持久化
- 使用 `datetime` 处理时间
- 使用 `dataclass` 定义数据结构
- 使用 `enum` 定义状态类型
- 基本的异常处理
- 代码组织：主逻辑、数据模型、存储逻辑分离

## 功能需求

### 1. 核心功能
- **添加任务** (`add`): 创建新任务，支持优先级和截止日期
- **列出任务** (`list`): 显示所有任务，支持按状态/优先级过滤
- **完成任务** (`done`): 标记任务为已完成
- **删除任务** (`delete`): 移除任务
- **编辑任务** (`edit`): 修改任务内容
- **查看任务详情** (`show`): 显示单个任务的详细信息

### 2. 数据结构
每个任务包含：
- `id`: 唯一标识符 (自增整数)
- `title`: 任务标题 (必填)
- `description`: 任务描述 (可选)
- `priority`: 优先级 (low/medium/high)
- `status`: 状态 (pending/done)
- `created_at`: 创建时间
- `due_date`: 截止日期 (可选)
- `completed_at`: 完成时间 (可选)

### 3. 命令行接口设计
```bash
# 添加任务
python todo.py add "买牛奶" --priority high --due 2024-01-15
python todo.py add "写报告" --desc "季度总结报告"

# 列出任务
python todo.py list
python todo.py list --status done
python todo.py list --priority high

# 完成任务
python todo.py done 1
python todo.py done 1 2 3

# 删除任务
python todo.py delete 1

# 编辑任务
python todo.py edit 1 --title "新标题" --priority low

# 查看详情
python todo.py show 1
```

### 4. 输出格式要求
- 列表显示使用表格格式对齐
- 状态用不同符号标识 (□ 待办，✓ 已完成)
- 优先级用颜色或文字标识
- 过期任务特殊标记

## 文件结构
```
project1_todo_cli/
├── PROJECT_REQUIREMENT.md    # 项目需求文档
├── todo.py                   # 主程序入口
├── models.py                 # 数据模型定义
├── storage.py                # 数据存储逻辑
└── data.json                 # 数据存储文件 (运行时创建)
```

## 验收标准
1. 所有命令能正常工作
2. 数据能正确保存到文件
3. 重启程序后数据不丢失
4. 输入验证和错误处理完善
5. 代码清晰，函数职责单一
6. 代码行数约 300-400 行

## 扩展挑战 (可选)
- 添加任务分类/标签功能
- 添加搜索功能
- 支持导出数据
- 添加统计信息 (完成数/待办数)
