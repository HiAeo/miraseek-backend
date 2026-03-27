from api import brands, tasks, results, reports, alerts
from fastapi import APIRouter

brands_router = brands.router
tasks_router = tasks.router
results_router = results.router
reports_router = reports.router
alerts_router = alerts.router
