"""
Pydantic 数据模型
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    active = "active"
    paused = "paused"


class AlertLevel(str, Enum):
    danger = "danger"
    warning = "warning"
    info = "info"


class AlertStatus(str, Enum):
    unread = "unread"
    read = "read"


# ========== 品牌模型 ==========
class BrandBase(BaseModel):
    brand_name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    core_technicals: Optional[List[str]] = []


class BrandCreate(BrandBase):
    competitors: Optional[List[int]] = []


class Brand(BrandBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 监控任务模型 ==========
class TaskBase(BaseModel):
    brand_id: int
    prompt_text: str
    prompt_type: str = "custom"
    ai_models: List[str] = ["deepseek"]
    frequency: str = "1d"


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 监控结果模型 ==========
class ResultBase(BaseModel):
    task_id: int
    ai_model: str
    rank: Optional[int] = None
    answer_text: Optional[str] = None
    sentiment_score: Optional[float] = None
    decision_stage: Optional[str] = None
    official_citation: Optional[bool] = False
    extracted_params: Optional[dict] = {}
    citations: Optional[List[str]] = []


class ResultCreate(ResultBase):
    pass


class Result(ResultBase):
    id: int
    query_timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 预警模型 ==========
class AlertRuleBase(BaseModel):
    brand_id: int
    rule_type: str
    threshold_value: Optional[float] = None
    notify_emails: Optional[List[str]] = []


class AlertRuleCreate(AlertRuleBase):
    pass


class AlertBase(BaseModel):
    rule_id: int
    message: str


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    triggered_at: datetime
    is_resolved: bool = False

    class Config:
        from_attributes = True


# ========== 报告模型 ==========
class ReportBase(BaseModel):
    brand_id: int
    report_type: str
    date_start: str
    date_end: str


class ReportCreate(ReportBase):
    pass


class Report(ReportBase):
    id: str
    status: str = "processing"
    download_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 统计响应模型 ==========
class KPICard(BaseModel):
    visibility_index: float
    visibility_trend: float
    total_mentions: int
    mentions_trend: float
    avg_sentiment: float
    sentiment_trend: float
    competitor_gap: float
    gap_trend: float


class VisibilityTrend(BaseModel):
    date: str
    value: float


class BrandRanking(BaseModel):
    rank: int
    brand: str
    mentions: int
    sentiment: float
    change: int


class DashboardData(BaseModel):
    kpi: KPICard
    visibility_trend: List[VisibilityTrend]
    brand_rankings: List[BrandRanking]
    ai_mentions: List[dict]
    latest_alerts: List[dict]
