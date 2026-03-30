# 命令行待办事项管理器

## 项目简介
一个功能完整的命令行待办事项管理应用，使用 JSON 文件存储数据。

## 代码结构
```
project1_todo_cli/
├── PROJECT_REQUIREMENT.md    # 项目需求文档
├── README.md                 # 本文件
├── todo.py                   # 主程序入口 (285 行)
├── models.py                 # 数据模型定义 (76 行)
├── storage.py                # 数据存储逻辑 (99 行)
└── data.json                 # 数据存储文件 (运行时创建)
```

**总代码行数：约 460 行**

## 使用方法

### 添加任务
```bash
# 基本用法
python todo.py add "买牛奶"

# 设置优先级
python todo.py add "写报告" --priority high

# 设置截止日期
python todo.py add "开会" --due 2024-12-31

# 完整示例
python todo.py add "完成项目" --desc "季度总结报告" --priority high --due 2024-12-31
```

### 列出任务
```bash
# 列出所有任务
python todo.py list

# 按状态过滤
python todo.py list --status pending
python todo.py list --status done

# 按优先级过滤
python todo.py list --priority high
```

### 完成任务
```bash
# 完成单个任务
python todo.py done 1

# 完成多个任务
python todo.py done 1 2 3
```

### 删除任务
```bash
python todo.py delete 1
```

### 编辑任务
```bash
# 修改标题
python todo.py edit 1 --title "新标题"

# 修改优先级
python todo.py edit 1 --priority low

# 修改多个字段
python todo.py edit 1 --title "新标题" --priority medium --due 2024-12-31
```

### 查看任务详情
```bash
python todo.py show 1
```

## 功能特性
- [x] 添加、删除、编辑任务
- [x] 任务状态管理（待办/已完成）
- [x] 优先级设置（低/中/高）
- [x] 截止日期设置
- [x] 过期任务提醒
- [x] 按状态/优先级过滤
- [x] 数据持久化（JSON 文件）
- [x] 命令行参数解析

## 涉及知识点
- `argparse` - 命令行参数解析
- `dataclass` - 数据类
- `enum` - 枚举类型
- `json` - 数据序列化
- `datetime` - 日期时间处理
- 文件 I/O 操作
- 异常处理

## 运行要求
- Python 3.7+
- 无需额外依赖（仅使用标准库）
