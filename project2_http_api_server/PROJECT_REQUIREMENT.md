# 项目二：HTTP REST API 服务器 (书籍管理 API)

## 项目概述
构建一个 RESTful 风格的 HTTP API 服务器，实现书籍的 CRUD 操作，包含认证、分页、过滤等高级功能。

## 技术要求
- 使用 `http.server` 或 `flask` 构建 HTTP 服务
- 使用 `json` 处理请求/响应
- 使用 `sqlite3` 数据库存储数据
- 使用 `functools.wraps` 实现装饰器
- 使用 `logging` 记录日志
- 使用 `re` 进行路由匹配或 URL 解析
- 使用 `contextlib` 管理资源
- 使用 `typing` 类型提示
- JWT 或 Token 基础认证
- 中间件模式实现日志/认证

## 功能需求

### 1. API 端点

#### 认证相关
```
POST   /api/auth/register    # 用户注册
POST   /api/auth/login       # 用户登录
```

#### 书籍资源
```
GET    /api/books            # 获取书籍列表 (支持分页、过滤、搜索)
POST   /api/books            # 创建新书籍
GET    /api/books/{id}       # 获取单本书籍详情
PUT    /api/books/{id}       # 更新书籍信息
PATCH  /api/books/{id}       # 部分更新书籍
DELETE /api/books/{id}       # 删除书籍
```

#### 用户相关
```
GET    /api/users/profile    # 获取当前用户信息
PUT    /api/users/profile    # 更新用户信息
```

### 2. 数据模型

#### User (用户)
- `id`: 主键
- `username`: 用户名 (唯一)
- `email`: 邮箱
- `password_hash`: 密码哈希
- `created_at`: 创建时间

#### Book (书籍)
- `id`: 主键
- `title`: 标题
- `author`: 作者
- `isbn`: ISBN 号
- `price`: 价格
- `stock`: 库存
- `category`: 分类
- `description`: 描述
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `owner_id`: 所有者 (外键关联 User)

### 3. 功能特性

#### 认证授权
- 密码使用 bcrypt 或 hashlib 加密
- 登录后返回 JWT token
- 受保护端点需要 Authorization header
- token 过期处理

#### 分页
```
GET /api/books?page=1&limit=10
```
响应包含：
- `data`: 数据列表
- `pagination`: 分页信息 (page, limit, total, total_pages)

#### 过滤和搜索
```
GET /api/books?author=鲁迅&category=小说&min_price=10&max_price=50
GET /api/books?q=python  # 搜索标题和描述
```

#### 排序
```
GET /api/books?sort=price&order=desc
GET /api/books?sort=created_at&order=desc
```

### 4. 响应格式

#### 成功响应
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}
```

#### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "资源不存在"
  }
}
```

#### HTTP 状态码
- 200: 成功
- 201: 创建成功
- 204: 删除成功 (无内容)
- 400: 请求参数错误
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器错误

### 5. 中间件
- **日志中间件**: 记录每个请求的方法、路径、耗时、状态码
- **认证中间件**: 验证 token，设置当前用户
- **错误处理中间件**: 统一错误响应格式
- **CORS 中间件**: 支持跨域请求

## 文件结构
```
project2_http_api_server/
├── PROJECT_REQUIREMENT.md    # 项目需求文档
├── app.py                    # 应用主入口
├── server.py                 # HTTP 服务器实现
├── router.py                 # 路由分发
├── handlers/
│   ├── __init__.py
│   ├── auth_handler.py       # 认证相关处理
│   ├── book_handler.py       # 书籍相关处理
│   └── user_handler.py       # 用户相关处理
├── models/
│   ├── __init__.py
│   ├── user.py               # 用户模型
│   └── book.py               # 书籍模型
├── middleware/
│   ├── __init__.py
│   ├── auth.py               # 认证中间件
│   ├── logger.py             # 日志中间件
│   └── error_handler.py      # 错误处理中间件
├── utils/
│   ├── __init__.py
│   ├── db.py                 # 数据库连接管理
│   ├── jwt.py                # JWT 工具
│   └── validators.py         # 参数验证
├── config.py                 # 配置管理
├── requirements.txt          # 依赖列表
└── books.db                  # SQLite 数据库 (运行时创建)
```

## 验收标准
1. 所有 API 端点正常工作
2. 认证机制安全可靠
3. 数据库操作正确，无 SQL 注入风险
4. 分页、过滤、搜索功能完善
5. 错误处理统一，响应格式一致
6. 日志记录完整
7. 代码组织清晰，模块化良好
8. 使用装饰器和中间件模式
9. 代码行数约 800-1200 行

## 扩展挑战 (可选)
- 添加速率限制 (Rate Limiting)
- 添加请求体大小限制
- 实现书籍借阅功能
- 添加单元测试
- 添加 API 文档 (OpenAPI/Swagger)
- 支持文件上传 (书籍封面)
