# 书籍管理 API 服务器

## 项目简介
一个 RESTful 风格的 HTTP API 服务器，实现书籍的 CRUD 操作，包含认证、分页、过滤等高级功能。

## 代码结构
```
project2_http_api_server/
├── PROJECT_REQUIREMENT.md    # 项目需求文档
├── README.md                 # 本文件
├── app.py                    # 应用主入口 (72 行)
├── server.py                 # HTTP 服务器实现 (194 行)
├── router.py                 # 路由分发 (102 行)
├── config.py                 # 配置管理 (26 行)
├── requirements.txt          # 依赖列表
├── handlers/
│   ├── __init__.py           # (10 行)
│   ├── auth_handler.py       # 认证处理 (80 行)
│   ├── book_handler.py       # 书籍处理 (249 行)
│   └── user_handler.py       # 用户处理 (58 行)
├── middleware/
│   ├── __init__.py           # (27 行)
│   ├── auth.py               # 认证中间件 (63 行)
│   ├── error_handler.py      # 错误处理 (71 行)
│   └── logger.py             # 日志中间件 (44 行)
├── models/
│   ├── __init__.py           # (10 行)
│   ├── user.py               # 用户模型 (124 行)
│   └── book.py               # 书籍模型 (183 行)
└── utils/
    ├── __init__.py           # (34 行)
    ├── db.py                 # 数据库管理 (93 行)
    ├── jwt.py                # JWT 工具 (97 行)
    └── validators.py         # 参数验证 (81 行)
```

**总代码行数：约 1600 行**

## 快速开始

### 1. 初始化数据库
```bash
python app.py init
```

### 2. 启动服务器
```bash
python app.py runserver
```

服务器默认运行在 `http://localhost:8080`

## API 端点

### 认证相关

#### 用户注册
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

#### 用户登录
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

响应：
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {...},
  "message": "登录成功"
}
```

### 书籍资源

#### 获取书籍列表
```bash
# 基本查询
GET /api/books

# 分页
GET /api/books?page=1&limit=10

# 按作者过滤
GET /api/books?author=鲁迅

# 按分类过滤
GET /api/books?category=编程

# 价格范围
GET /api/books?min_price=50&max_price=100

# 搜索
GET /api/books?q=python

# 排序
GET /api/books?sort=price&order=desc
```

#### 获取单本书籍
```bash
GET /api/books/1
```

#### 创建书籍（需认证）
```bash
POST /api/books
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Python 编程",
  "author": "Eric Matthes",
  "isbn": "978-7-115-42802-8",
  "price": 89.0,
  "stock": 10,
  "category": "编程",
  "description": "Python 入门经典"
}
```

#### 更新书籍（全量，需认证）
```bash
PUT /api/books/1
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Python 编程（第 2 版）",
  "author": "Eric Matthes",
  "price": 99.0
}
```

#### 部分更新书籍（需认证）
```bash
PATCH /api/books/1
Content-Type: application/json
Authorization: Bearer <token>

{
  "stock": 20
}
```

#### 删除书籍（需认证）
```bash
DELETE /api/books/1
Authorization: Bearer <token>
```

### 用户相关

#### 获取个人信息（需认证）
```bash
GET /api/users/profile
Authorization: Bearer <token>
```

#### 更新个人信息（需认证）
```bash
PUT /api/users/profile
Content-Type: application/json
Authorization: Bearer <token>

{
  "email": "newemail@example.com"
}
```

## 响应格式

### 成功响应
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}
```

### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "资源不存在"
  }
}
```

### HTTP 状态码
| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 500 | 服务器错误 |

## 功能特性
- [x] RESTful API 设计
- [x] JWT 认证
- [x] 用户注册/登录
- [x] 书籍 CRUD 操作
- [x] 分页查询
- [x] 多条件过滤
- [x] 全文搜索
- [x] 排序功能
- [x] 请求日志
- [x] 统一错误处理
- [x] CORS 支持
- [x] 中间件模式
- [x] 装饰器模式

## 涉及知识点
- `http.server` - HTTP 服务器
- `sqlite3` - 数据库
- `json` - 数据序列化
- `hashlib/hmac` - 密码加密/JWT
- `functools.wraps` - 装饰器
- `contextlib` - 上下文管理器
- `typing` - 类型提示
- `re` - 正则表达式
- `logging` - 日志记录
- 装饰器模式
- 中间件模式
- MVC 架构
- RESTful 设计

## 运行要求
- Python 3.9+
- 无需额外依赖（仅使用标准库）

## 测试账号
初始化数据库后会自动创建：
- 用户名：`admin`
- 密码：`admin123`
