# 论文格式检测系统 - 安装部署文档

## 目录

1. [系统要求](#系统要求)
2. [Docker 部署（推荐）](#docker-部署推荐)
3. [本地开发环境搭建](#本地开发环境搭建)
4. [生产环境部署](#生产环境部署)
5. [常见安装问题](#常见安装问题)

---

## 系统要求

### 硬件要求

| 配置 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 2核 | 4核+ |
| 内存 | 4GB | 8GB+ |
| 硬盘 | 20GB | 50GB+ |
| 网络 | 10Mbps | 100Mbps+ |

### 软件要求

#### Docker 部署
- Docker 20.10+
- Docker Compose 2.0+

#### 本地开发
- Python 3.12+
- Node.js 18+
- MySQL 8.0+
- Git

### 操作系统支持
- Linux (Ubuntu 20.04+, CentOS 7+)
- macOS 10.15+
- Windows 10+ (WSL2 推荐)

---

## Docker 部署（推荐）

### 1. 安装 Docker 和 Docker Compose

#### Linux (Ubuntu)
```bash
# 更新包索引
sudo apt-get update

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

#### macOS
```bash
# 下载并安装 Docker Desktop for Mac
# 访问: https://www.docker.com/products/docker-desktop
```

#### Windows
```bash
# 下载并安装 Docker Desktop for Windows
# 访问: https://www.docker.com/products/docker-desktop
# 启用 WSL2 后端
```

### 2. 获取项目代码

```bash
# 克隆项目
git clone <repository-url>
cd paper_check
```

### 3. 配置环境变量

#### 后端配置
```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件：
```env
# 数据库配置
DB_HOST=mysql
DB_PORT=3306
DB_NAME=paper_check_db
DB_USER=root
DB_PASSWORD=123456

# JWT 配置
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# 应用配置
APP_NAME=论文格式检测系统
APP_VERSION=1.0.0
DEBUG=false

# 文件上传配置
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=52428800

# OSS 配置（可选）
OSS_ACCESS_KEY_ID=your_oss_access_key
OSS_ACCESS_KEY_SECRET=your_oss_secret
OSS_BUCKET_NAME=your_bucket_name
OSS_ENDPOINT=your_oss_endpoint

# Redis 配置（可选）
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

#### 前端配置
```bash
cd ../frontend
cp .env.development.example .env.development
cp .env.production.example .env.production
```

编辑 `.env.development`：
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=论文格式检测系统
```

编辑 `.env.production`：
```env
VITE_API_BASE_URL=https://your-domain.com/api/v1
VITE_APP_TITLE=论文格式检测系统
```

### 4. 修改 Docker Compose 配置

编辑 `docker-compose.yml` 文件，根据需要调整配置：

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: paper_check_mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: 123456  # 修改为强密码
      MYSQL_DATABASE: paper_check_db
      MYSQL_USER: paper_check
      MYSQL_PASSWORD: paper_password  # 修改为强密码
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./backend/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    command: --default-authentication-plugin=mysql_native_password --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: paper_check_backend
    restart: unless-stopped
    environment:
      DB_HOST: mysql
      DB_PORT: 3306
      DB_NAME: paper_check_db
      DB_USER: root
      DB_PASSWORD: 123456
      JWT_SECRET_KEY: your-super-secret-key-change-in-production
      DEBUG: "false"
    ports:
      - "8000:8000"
    depends_on:
      mysql:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - uploads:/app/uploads

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: paper_check_frontend
    restart: unless-stopped
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mysql_data:
  uploads:
```

### 5. 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 6. 初始化数据库

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行数据库迁移
alembic upgrade head

# 初始化数据（可选）
python scripts/init_db.py

# 退出容器
exit
```

### 7. 验证安装

访问以下地址验证服务是否正常运行：

- 前端页面: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 8. 常用 Docker 命令

```bash
# 停止服务
docker-compose stop

# 启动服务
docker-compose start

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec [service_name] bash

# 删除所有容器和数据
docker-compose down -v

# 重新构建镜像
docker-compose build --no-cache
```

---

## 本地开发环境搭建

### 1. 安装依赖软件

#### Python 3.12+
```bash
# Linux (Ubuntu)
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv python3-pip

# macOS
brew install python@3.12

# Windows
# 下载并安装 Python 3.12 from python.org
```

#### Node.js 18+
```bash
# Linux (Ubuntu)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node

# Windows
# 下载并安装 Node.js from nodejs.org
```

#### MySQL 8.0+
```bash
# Linux (Ubuntu)
sudo apt-get install mysql-server

# macOS
brew install mysql

# Windows
# 下载并安装 MySQL from mysql.com
```

### 2. 配置数据库

```bash
# 启动 MySQL 服务
sudo systemctl start mysql  # Linux
brew services start mysql    # macOS

# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE paper_check_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选）
CREATE USER 'paper_check'@'localhost' IDENTIFIED BY 'paper_password';
GRANT ALL PRIVILEGES ON paper_check_db.* TO 'paper_check'@'localhost';
FLUSH PRIVILEGES;

# 退出 MySQL
EXIT;
```

### 3. 后端开发环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库连接等信息

# 运行数据库迁移
alembic upgrade head

# 初始化数据（可选）
python scripts/init_db.py

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 前端开发环境

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.development.example .env.development
# 编辑 .env.development 文件

# 启动开发服务器
npm run dev
```

### 5. 开发工具推荐

#### 后端开发
- **IDE**: PyCharm Professional / VS Code
- **数据库工具**: DBeaver / MySQL Workbench
- **API 测试**: Postman / Insomnia

#### 前端开发
- **IDE**: VS Code / WebStorm
- **浏览器**: Chrome DevTools
- **调试工具**: React Developer Tools

### 6. 开发工作流

#### 后端开发流程
```bash
# 1. 创建功能分支
git checkout -b feature/your-feature

# 2. 修改代码
# 编辑相关文件

# 3. 运行测试（如果有）
pytest

# 4. 创建数据库迁移
alembic revision --autogenerate -m "your migration message"
alembic upgrade head

# 5. 提交代码
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

#### 前端开发流程
```bash
# 1. 创建功能分支
git checkout -b feature/your-feature

# 2. 修改代码
# 编辑相关文件

# 3. 运行开发服务器
npm run dev

# 4. 构建测试
npm run build

# 5. 提交代码
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

---

## 生产环境部署

### 1. 服务器准备

#### 安全配置
```bash
# 更新系统
sudo apt-get update && sudo apt-get upgrade -y

# 配置防火墙
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# 创建部署用户
sudo adduser deploy
sudo usermod -aG sudo deploy
sudo usermod -aG docker deploy
```

### 2. 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 配置用户权限
sudo usermod -aG docker $USER
```

### 3. 部署应用

```bash
# 克隆项目
git clone <repository-url> /opt/paper_check
cd /opt/paper_check

# 配置环境变量
cd backend
cp .env.example .env
# 编辑 .env 文件，设置生产环境配置

# 修改 docker-compose.yml
# - 设置强密码
# - 配置正确的域名
# - 设置 DEBUG=false

# 启动服务
docker-compose up -d

# 初始化数据库
docker-compose exec backend alembic upgrade head
```

### 4. 配置 Nginx 反向代理

```bash
# 安装 Nginx
sudo apt-get install nginx -y

# 创建配置文件
sudo nano /etc/nginx/sites-available/paper_check
```

Nginx 配置示例：
```nginx
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name your-domain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL 证书配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 前端静态文件
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 文件上传大小限制
        client_max_body_size 50M;
    }

    # 上传文件
    location /uploads/ {
        alias /opt/paper_check/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/paper_check /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

### 5. 配置 HTTPS

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# 获取 SSL 证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 6. 配置自动备份

```bash
# 创建备份脚本
sudo nano /opt/backup.sh
```

备份脚本示例：
```bash
#!/bin/bash

# 配置
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
MYSQL_CONTAINER="paper_check_mysql"
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DATABASE="paper_check_db"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker exec $MYSQL_CONTAINER mysqldump -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > $BACKUP_DIR/db_$DATE.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /opt/paper_check/uploads

# 删除 7 天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# 设置执行权限
sudo chmod +x /opt/backup.sh

# 添加定时任务
sudo crontab -e
```

添加定时任务（每天凌晨 2 点备份）：
```
0 2 * * * /opt/backup.sh >> /var/log/backup.log 2>&1
```

### 7. 监控和日志

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 配置日志轮转
sudo nano /etc/logrotate.d/paper_check
```

日志轮转配置：
```
/opt/paper_check/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 deploy deploy
}
```

---

## 常见安装问题

### 1. Docker 相关问题

#### 问题：Docker 服务无法启动
```bash
# 检查 Docker 状态
sudo systemctl status docker

# 启动 Docker
sudo systemctl start docker

# 查看错误日志
sudo journalctl -u docker
```

#### 问题：容器启动失败
```bash
# 查看容器日志
docker-compose logs [service_name]

# 重新构建镜像
docker-compose build --no-cache [service_name]

# 清理并重新启动
docker-compose down -v
docker-compose up -d
```

### 2. 数据库相关问题

#### 问题：数据库连接失败
```bash
# 检查 MySQL 容器状态
docker-compose ps mysql

# 查看数据库日志
docker-compose logs mysql

# 测试数据库连接
docker-compose exec mysql mysql -u root -p
```

#### 问题：数据库迁移失败
```bash
# 检查迁移状态
docker-compose exec backend alembic current

# 重置迁移（谨慎使用）
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head
```

### 3. 网络相关问题

#### 问题：端口被占用
```bash
# 查看端口占用
sudo netstat -tulpn | grep :8000
sudo lsof -i :8000

# 修改 docker-compose.yml 中的端口映射
```

#### 问题：跨域问题
```bash
# 检查后端 CORS 配置
# 编辑 backend/app/main.py
# 确保 CORS 中间件配置正确
```

### 4. 文件权限问题

#### 问题：上传文件权限不足
```bash
# 修改上传目录权限
sudo chown -R $USER:$USER ./uploads
sudo chmod -R 755 ./uploads

# Docker 容器内权限
docker-compose exec backend chown -R appuser:appuser /app/uploads
```

### 5. 性能优化建议

#### 后端优化
```bash
# 增加 worker 数量
# 修改 docker-compose.yml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 配置数据库连接池
# 编辑 backend/app/database.py
```

#### 前端优化
```bash
# 启用生产构建
npm run build

# 配置 CDN
# 修改 nginx 配置
```

---

## 技术支持

如果遇到安装问题，请通过以下方式获得帮助：

- **文档**: 查看项目 README.md
- **Issue**: 在 GitHub 提交问题
- **邮件**: support@example.com
- **社区**: 访问用户论坛

---

**祝您部署顺利！**