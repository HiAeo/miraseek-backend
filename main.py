"""
MiraSeek Backend API
FastAPI + Supabase
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from api import register_routes

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
register_routes(app)


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
