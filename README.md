# 论文格式检测系统

基于 FastAPI + React 的论文格式智能检测与自动修复系统

## 项目简介

本系统旨在帮助学生和教师快速检测论文格式问题，并提供自动修复功能。支持多种格式规范检测，包括字体、字号、行距、缩进、段落间距等常见格式问题。

### 主要功能

- **论文格式检测**: 自动检测 Word 文档中的格式问题
- **智能修复**: 一键修复可自动处理的格式问题
- **模板管理**: 支持自定义格式模板和规则配置
- **班级管理**: 教师可创建班级，管理学生论文提交
- **会员系统**: 支持免费/付费会员体系
- **批量检测**: 支持多篇论文批量检测

## 技术栈

### 后端
| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.12+ | 编程语言 |
| FastAPI | 0.109.2 | Web 框架 |
| SQLAlchemy | 2.0.25 | ORM 框架 |
| MySQL | 8.0+ | 数据库 |
| python-docx | 1.1.0 | Word 文档处理 |
| JWT | 3.3.0 | 身份认证 |
| Alembic | 1.13.1 | 数据库迁移 |

### 前端
| 技术 | 版本 | 说明 |
|------|------|------|
| React | 18.2+ | 前端框架 |
| TypeScript | 5.3+ | 类型安全 |
| Vite | 5.1+ | 构建工具 |
| Ant Design | 5.15+ | UI 组件库 |
| Redux Toolkit | 2.2+ | 状态管理 |
| React Router | 6.22+ | 路由管理 |

## 项目结构

```
paper_check/
├── backend/                 # 后端代码
│   ├── app/                 # 应用核心代码
│   │   ├── api/             # API 路由
│   │   │   └── v1/          # v1 版本 API
│   │   ├── core/            # 核心配置（安全、异常处理）
│   │   ├── models/          # 数据库模型
│   │   ├── schemas/         # Pydantic 数据模型
│   │   ├── services/        # 业务逻辑服务
│   │   ├── utils/           # 工具函数（文档解析、格式检测）
│   │   ├── config.py        # 配置文件
│   │   ├── database.py      # 数据库连接
│   │   └── main.py          # 应用入口
│   ├── alembic/             # 数据库迁移
│   ├── scripts/             # 脚本工具
│   ├── requirements.txt     # Python 依赖
│   └── Dockerfile           # 后端 Docker 配置
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── api/             # API 请求封装
│   │   ├── components/      # 公共组件
│   │   ├── pages/           # 页面组件
│   │   ├── router/          # 路由配置
│   │   ├── store/           # Redux 状态管理
│   │   ├── types/           # TypeScript 类型定义
│   │   └── utils/           # 工具函数
│   ├── package.json         # 前端依赖
│   └── Dockerfile           # 前端 Docker 配置
├── uploads/                 # 上传文件存储目录
├── docker-compose.yml       # Docker Compose 配置
└── README.md                # 项目说明文档
```

## 快速开始

### 环境要求

- Docker 20.10+
- Docker Compose 2.0+

### 启动项目

1. **克隆项目**
```bash
git clone <repository-url>
cd paper_check
```

2. **启动容器**
```bash
docker-compose up -d
```

3. **等待服务启动**
- 后端服务: http://localhost:8000
- 前端服务: http://localhost:3000
- API 文档: http://localhost:8000/docs

### 本地开发

#### 后端开发

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

## API 接口

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/login | 用户登录 |
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/logout | 用户登出 |

### 论文接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/papers/upload | 上传论文 |
| GET | /api/v1/papers | 获取论文列表 |
| GET | /api/v1/papers/{id} | 获取论文详情 |
| DELETE | /api/v1/papers/{id} | 删除论文 |

### 检测接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/papers/{id}/check | 检测论文格式 |
| GET | /api/v1/check/{result_id} | 获取检测结果详情 |
| POST | /api/v1/check/{result_id}/fix/one-click | 一键修复 |

### 班级接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/classes | 创建班级 |
| GET | /api/v1/classes | 获取班级列表 |
| POST | /api/v1/classes/{id}/join | 加入班级 |

## 核心功能模块

### 1. 格式检测引擎

支持检测以下格式问题：
- 字体类型和大小
- 行间距设置
- 段落缩进
- 首行缩进
- 段前段后距
- 页眉页脚
- 页码格式

### 2. 自动修复功能

根据检测结果自动修复可处理的格式问题，保留原文件，生成修复后的新文件。

### 3. 模板系统

支持自定义格式模板，可配置检测规则和修复策略。

### 4. 会员体系

| 会员等级 | 每日检测次数 | 自动修复 |
|----------|-------------|---------|
| 免费用户 | 3次 | 不可用 |
| 基础会员 | 不限 | 有限次数 |
| 高级会员 | 不限 | 无限制 |

## 数据库设计

### 核心表结构

- `users` - 用户表
- `papers` - 论文表
- `check_results` - 检测结果表
- `check_issues` - 检测问题明细表
- `templates` - 模板表
- `classes` - 班级表
- `vip_members` - VIP 会员表

## 配置说明

### 环境变量

后端配置文件 `.env`:
```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=paper_check_db
DB_USER=paper_check
DB_PASSWORD=paper_password

# JWT 配置
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256

# 应用配置
APP_NAME=论文格式检测系统
APP_VERSION=1.0.0
DEBUG=true

# 文件上传配置
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800
```

## 开发流程

### 后端开发

1. 创建数据库模型 (`app/models/`)
2. 创建数据模型 (`app/schemas/`)
3. 实现业务逻辑 (`app/services/`)
4. 创建 API 路由 (`app/api/v1/`)
5. 编写数据库迁移 (`alembic revision`)

### 前端开发

1. 创建页面组件 (`src/pages/`)
2. 封装 API 请求 (`src/api/`)
3. 配置路由 (`src/router/`)
4. 添加状态管理 (`src/store/`)

## 部署

### 生产环境部署

1. 修改 `.env` 配置文件
2. 构建 Docker 镜像
3. 使用 Nginx 反向代理
4. 配置 HTTPS 证书

### Docker 部署

```bash
docker-compose -f docker-compose.yml up -d
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！


