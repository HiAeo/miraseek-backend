from fastapi import APIRouter
from api import brands, tasks, results, reports, alerts

# 注册所有路由
brands_router = brands.router
tasks_router = tasks.router
results_router = results.router
reports_router = reports.router
alerts_router = alerts.router

# 主路由注册函数
def register_routes(app):
    app.include_router(brands_router, prefix="/api/v1/brands", tags=["品牌管理"])
    app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["监控任务"])
    app.include_router(results_router, prefix="/api/v1/results", tags=["监控结果"])
    app.include_router(reports_router, prefix="/api/v1/reports", tags=["报告中心"])
    app.include_router(alerts_router, prefix="/api/v1/alerts", tags=["预警中心"])
