"""
MiraSeek Backend API
FastAPI + Supabase
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from api import brands_router, tasks_router, results_router, reports_router, alerts_router

app = FastAPI(
    title="MiraSeek API",
    description="AI可见性监控平台后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有路由
app.include_router(brands_router, prefix="/api/v1/brands", tags=["品牌管理"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["监控任务"])
app.include_router(results_router, prefix="/api/v1/results", tags=["监控结果"])
app.include_router(reports_router, prefix="/api/v1/reports", tags=["报告中心"])
app.include_router(alerts_router, prefix="/api/v1/alerts", tags=["预警中心"])


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def root():
    return {
        "name": "MiraSeek API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
