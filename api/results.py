"""
监控结果 API + 仪表盘数据
"""
from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timedelta
import random
from core.database import get_supabase
from models.schemas import Result, ResultCreate, DashboardData

router = APIRouter()


@router.get("/")
async def get_results(
    task_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """获取监控结果列表"""
    supabase = get_supabase()
    query = supabase.table("miraseek_results").select("*")
    
    if task_id:
        query = query.eq("task_id", task_id)
    if brand_id:
        query = query.eq("brand_id", brand_id)
    
    result = query.order("query_timestamp", desc=True).range(skip, skip + limit - 1).execute()
    return {"code": 0, "data": {"total": len(result.data), "items": result.data}}


@router.get("/dashboard")
async def get_dashboard(brand_id: int = Query(1)):
    """获取仪表盘数据（含 KPI、趋势、排行榜等）"""
    supabase = get_supabase()
    
    # 尝试从数据库获取真实数据
    try:
        # 获取最近的监控结果
        results = supabase.table("miraseek_results").select("*").eq("brand_id", brand_id).limit(100).execute()
        
        if results.data:
            # 计算真实 KPI
            total_mentions = len(results.data)
            avg_sentiment = sum(r.get("sentiment_score", 0) for r in results.data if r.get("sentiment_score")) / max(total_mentions, 1)
            avg_rank = sum(r.get("rank", 0) for r in results.data if r.get("rank")) / max(len([r for r in results.data if r.get("rank")]), 1)
            
            visibility_index = round(100 - avg_rank * 10 + avg_sentiment * 10, 1)
        else:
            # 无数据时返回模拟数据
            return get_mock_dashboard()
    except Exception as e:
        # 数据库无数据或出错，返回模拟数据
        return get_mock_dashboard()
    
    # 构建响应
    return {
        "code": 0,
        "data": {
            "kpi": {
                "visibility_index": visibility_index if results.data else 78.5,
                "visibility_trend": 12.3,
                "total_mentions": total_mentions if results.data else 2847,
                "mentions_trend": 8.5,
                "avg_sentiment": round(avg_sentiment, 2) if results.data else 0.82,
                "sentiment_trend": -2.1,
                "competitor_gap": 13.5,
                "gap_trend": -3.2
            },
            "visibility_trend": generate_trend_data(),
            "brand_rankings": get_mock_rankings(),
            "ai_mentions": get_mock_ai_mentions(),
            "latest_alerts": get_mock_alerts()
        }
    }


def get_mock_dashboard():
    """返回模拟仪表盘数据"""
    return {
        "code": 0,
        "data": {
            "kpi": {
                "visibility_index": 78.5,
                "visibility_trend": 12.3,
                "total_mentions": 2847,
                "mentions_trend": 8.5,
                "avg_sentiment": 0.82,
                "sentiment_trend": -2.1,
                "competitor_gap": 13.5,
                "gap_trend": -3.2
            },
            "visibility_trend": generate_trend_data(),
            "brand_rankings": get_mock_rankings(),
            "ai_mentions": get_mock_ai_mentions(),
            "latest_alerts": get_mock_alerts()
        }
    }


def generate_trend_data():
    """生成30天趋势数据"""
    data = []
    for i in range(30, 0, -1):
        date = datetime.now() - timedelta(days=i)
        value = 65 + random.random() * 20 + (30 - i) * 0.3
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": round(value, 1)
        })
    return data


def get_mock_rankings():
    """模拟品牌排行榜"""
    return [
        {"rank": 1, "brand": "汇川技术", "mentions": 892, "sentiment": 0.91, "change": 0},
        {"rank": 2, "brand": "MiraSeek", "mentions": 684, "sentiment": 0.82, "change": 1},
        {"rank": 3, "brand": "ABB", "mentions": 645, "sentiment": 0.78, "change": -1},
        {"rank": 4, "brand": "西门子", "mentions": 598, "sentiment": 0.85, "change": 0},
        {"rank": 5, "brand": "发那科", "mentions": 523, "sentiment": 0.76, "change": 2},
    ]


def get_mock_ai_mentions():
    """模拟AI模型提及分布"""
    return [
        {"model": "DeepSeek", "value": 38, "count": 1082},
        {"model": "Kimi", "value": 28, "count": 797},
        {"model": "豆包", "value": 18, "count": 512},
        {"model": "文心一言", "value": 12, "count": 341},
        {"model": "通义千问", "value": 4, "count": 115}
    ]


def get_mock_alerts():
    """模拟最新预警"""
    return [
        {
            "id": 1,
            "type": "rank_drop",
            "level": "warning",
            "title": "排名下降预警",
            "message": "在提示词中品牌排名从第2位下降至第3位",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "unread"
        },
        {
            "id": 2,
            "type": "negative_sentiment",
            "level": "danger",
            "title": "负面情感预警",
            "message": "DeepSeek回答中出现关于售后服务响应慢的负面评价",
            "time": (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
            "status": "unread"
        }
    ]


@router.post("/")
async def create_result(result: ResultCreate):
    """创建监控结果"""
    supabase = get_supabase()
    data = result.model_dump()
    data["query_timestamp"] = datetime.now().isoformat()
    result = supabase.table("miraseek_results").insert(data).execute()
    return {"code": 0, "message": "success", "data": result.data[0]}
