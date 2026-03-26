# MiraSeek Backend - AI可见性监控平台后端API

基于 FastAPI + Supabase 的后端服务。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env` 文件并填写：

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. 初始化数据库

在 Supabase Dashboard > SQL Editor 中执行 `init_db.sql`。

### 4. 启动服务

```bash
uvicorn main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/brands` | GET/POST | 品牌管理 |
| `/api/v1/tasks` | GET/POST | 监控任务 |
| `/api/v1/results` | GET | 监控结果 |
| `/api/v1/results/dashboard` | GET | 仪表盘数据 |
| `/api/v1/reports` | GET/POST | 报告中心 |
| `/api/v1/alerts` | GET | 预警中心 |

## 部署

支持部署到：
- Render (推荐，免费)
- Railway
- Fly.io
- Heroku
