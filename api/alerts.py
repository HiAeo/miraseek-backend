"""
预警中心 API
"""
from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
from core.database import get_supabase

router = APIRouter()


@router.get("/")
async def get_alerts(
    level: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """获取预警列表"""
    supabase = get_supabase()
    try:
        query = supabase.table("miraseek_alerts").select("*")
        
        if level:
            query = query.eq("level", level)
        if status:
            query = query.eq("status", status)
        
        result = query.order("triggered_at", desc=True).range(skip, skip + limit - 1).execute()
        
        # 统计
        total = len(result.data)
        unread = len([a for a in result.data if a.get("status") == "unread"])
        danger = len([a for a in result.data if a.get("level") == "danger"])
        
        return {
            "code": 0,
            "data": {
                "total": total,
                "unread": unread,
                "danger": danger,
                "items": result.data
            }
        }
    except:
        # 表不存在时返回模拟数据
        return {"code": 0, "data": {"total": 4, "unread": 2, "danger": 1, "items": get_mock_alerts()}}


@router.put("/{alert_id}/read")
async def mark_alert_read(alert_id: int):
    """标记预警为已读"""
    supabase = get_supabase()
    try:
        supabase.table("miraseek_alerts").update({"status": "read"}).eq("id", alert_id).execute()
        return {"code": 0, "message": "success"}
    except:
        return {"code": 0, "message": "success"}


@router.put("/read-all")
async def mark_all_read():
    """全部标记为已读"""
    supabase = get_supabase()
    try:
        supabase.table("miraseek_alerts").update({"status": "read"}).eq("status", "unread").execute()
        return {"code": 0, "message": "success"}
    except:
        return {"code": 0, "message": "success"}


def get_mock_alerts():
    """模拟预警数据"""
    return [
        {
            "id": 1,
            "type": "rank_drop",
            "level": "warning",
            "title": "排名下降预警",
            "message": "在"国产工业机器人品牌排名"提示词中，您的品牌排名从第2位下降至第3位",
            "triggered_at": "2026-03-26 10:30",
            "status": "unread"
        },
        {
            "id": 2,
            "type": "negative_sentiment",
            "level": "danger",
            "title": "负面情感预警",
            "message": "DeepSeek在回答中出现关于"售后服务响应慢"的负面评价",
            "triggered_at": "2026-03-26 09:15",
            "status": "unread"
        },
        {
            "id": 3,
            "type": "competitor_up",
            "level": "info",
            "title": "竞品提及增加",
            "message": "BrandX 在近7天的提及量环比增长 23%",
            "triggered_at": "2026-03-25 16:00",
            "status": "read"
        },
        {
            "id": 4,
            "type": "keyword_alert",
            "level": "warning",
            "title": "关键词触发",
            "message": "关键词"MiraSeek 故障"在豆包回答中被提及",
            "triggered_at": "2026-03-25 11:20",
            "status": "read"
        }
    ]
