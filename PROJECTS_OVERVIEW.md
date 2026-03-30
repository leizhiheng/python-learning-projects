# Python 学习验收项目总览

为你设计了两个 Python 学习验收项目，难度递进，涵盖 Python 核心知识点。

---

## 项目对比

| 特性 | 项目一：Todo CLI | 项目二：HTTP API Server |
|------|-----------------|------------------------|
| 类型 | 命令行应用 | Web API 服务器 |
| 代码行数 | ~460 行 | ~1600 行 |
| 难度 | 入门 | 进阶 |
| 数据存储 | JSON 文件 | SQLite 数据库 |
| 核心模块 | argparse, json, dataclass | http.server, sqlite3, jwt |
| 设计模式 | 简单分层 | MVC + 中间件 + 装饰器 |

---

## 项目一：命令行待办事项管理器

### 项目位置
`project1_todo_cli/`

### 实现的功能
1. 添加任务（支持优先级、截止日期）
2. 列出任务（支持按状态/优先级过滤）
3. 完成任务
4. 删除任务
5. 编辑任务
6. 查看任务详情

### 涉及知识点
- `argparse` - 命令行参数解析
- `dataclass` - 数据类
- `enum` - 枚举类型
- `json` - 数据序列化
- `datetime` - 日期时间处理
- 文件 I/O 操作
- 异常处理

### 文件结构
```
project1_todo_cli/
├── PROJECT_REQUIREMENT.md    # 详细需求文档
├── README.md                 # 使用说明
├── todo.py                   # 主程序入口
├── models.py                 # 数据模型
├── storage.py                # 数据存储
└── data.json                 # 数据文件 (运行时创建)
```

### 运行示例
```bash
cd project1_todo_cli

# 添加任务
python todo.py add "学习 Python" --priority high
python todo.py add "完成项目" --due 2024-12-31

# 列出任务
python todo.py list
python todo.py list --status pending

# 完成任务
python todo.py done 1

# 编辑任务
python todo.py edit 1 --priority low

# 删除任务
python todo.py delete 1
```

---

## 项目二：HTTP REST API 服务器

### 项目位置
`project2_http_api_server/`

### 实现的功能
1. 用户注册/登录（JWT 认证）
2. 书籍资源 CRUD
3. 分页查询
4. 多条件过滤
5. 全文搜索
6. 排序功能
7. 请求日志
8. 统一错误处理

### 涉及知识点
- `http.server` - HTTP 服务器
- `sqlite3` - 数据库
- `json` - 数据序列化
- `hashlib/hmac` - 密码加密/JWT
- `functools.wraps` - 装饰器
- `contextlib` - 上下文管理器
- `typing` - 类型提示
- `re` - 正则表达式
- 装饰器模式
- 中间件模式
- MVC 架构
- RESTful 设计

### 文件结构
```
project2_http_api_server/
├── PROJECT_REQUIREMENT.md    # 详细需求文档
├── README.md                 # 使用说明
├── app.py                    # 主入口
├── server.py                 # HTTP 服务器
├── router.py                 # 路由分发
├── config.py                 # 配置管理
├── handlers/                 # 请求处理器
│   ├── auth_handler.py
│   ├── book_handler.py
│   └── user_handler.py
├── middleware/               # 中间件
│   ├── auth.py
│   ├── logger.py
│   └── error_handler.py
├── models/                   # 数据模型
│   ├── user.py
│   └── book.py
└── utils/                    # 工具函数
    ├── db.py
    ├── jwt.py
    └── validators.py
```

### 运行示例
```bash
cd project2_http_api_server

# 初始化数据库（创建测试数据）
python app.py init

# 启动服务器
python app.py runserver
```

### API 测试示例
```bash
# 登录获取 token
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 获取书籍列表
curl http://localhost:8080/api/books

# 创建书籍（需认证）
curl -X POST http://localhost:8080/api/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"新书","author":"作者"}'
```

---

## 学习建议

### 项目一（入门）
1. 先阅读 `PROJECT_REQUIREMENT.md` 了解需求
2. 尝试自己实现核心功能
3. 对比参考实现，学习：
   - 如何组织代码结构
   - 如何使用 dataclass 和 enum
   - 如何处理命令行参数
   - 如何持久化数据

### 项目二（进阶）
1. 确保已掌握项目一的知识点
2. 阅读 `PROJECT_REQUIREMENT.md` 了解 API 设计
3. 尝试自己实现，重点关注：
   - HTTP 协议基础
   - RESTful API 设计原则
   - 认证机制（JWT）
   - 装饰器和中间件模式
   - 数据库操作
   - 错误处理

### 对比学习点
- 代码组织方式
- 错误处理策略
- 数据验证方法
- 代码复用技巧

---

## 验收标准

### 项目一
- [ ] 所有命令正常工作
- [ ] 数据正确保存和加载
- [ ] 输入验证和错误处理完善
- [ ] 代码清晰，函数职责单一
- [ ] 代码行数 300-400 行左右

### 项目二
- [ ] 所有 API 端点正常工作
- [ ] 认证机制安全
- [ ] 数据库操作正确，无 SQL 注入风险
- [ ] 分页、过滤、搜索功能完善
- [ ] 错误处理统一
- [ ] 代码模块化良好
- [ ] 使用装饰器和中间件模式
- [ ] 代码行数 800-1200 行左右

---

**祝你学习愉快！**
