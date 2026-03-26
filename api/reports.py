"""
报告中心 API
"""
from fastapi import APIRouter
from datetime import datetime
import uuid
from core.database import get_supabase

router = APIRouter()


@router.get("/")
async def get_reports():
    """获取报告列表"""
    supabase = get_supabase()
    try:
        result = supabase.table("miraseek_reports").select("*").order("created_at", desc=True).limit(20).execute()
        return {"code": 0, "data": result.data}
    except:
        # 表不存在时返回模拟数据
        return {"code": 0, "data": get_mock_reports()}


@router.post("/generate")
async def generate_report(brand_id: int, report_type: str, date_start: str, date_end: str):
    """生成报告"""
    supabase = get_supabase()
    report_id = f"rep_{uuid.uuid4().hex[:12]}"
    
    data = {
        "id": report_id,
        "brand_id": brand_id,
        "report_type": report_type,
        "date_start": date_start,
        "date_end": date_end,
        "status": "processing",
        "created_at": datetime.now().isoformat()
    }
    
    try:
        result = supabase.table("miraseek_reports").insert(data).execute()
        return {"code": 0, "data": {"report_id": report_id, "status": "processing"}}
    except:
        return {"code": 0, "data": {"report_id": report_id, "status": "processing"}}


@router.get("/{report_id}")
async def get_report(report_id: str):
    """获取报告详情"""
    supabase = get_supabase()
    try:
        result = supabase.table("miraseek_reports").select("*").eq("id", report_id).execute()
        if result.data:
            return {"code": 0, "data": result.data[0]}
    except:
        pass
    return {"code": 404, "message": "Report not found"}


def get_mock_reports():
    """模拟报告数据"""
    return [
        {
            "id": "rep_001",
            "name": "2026年3月第三周周报",
            "type": "周报",
            "brand_id": 1,
            "date_range": "2026-03-17 ~ 2026-03-23",
            "created_at": "2026-03-24 09:00",
            "status": "ready"
        },
        {
            "id": "rep_002",
            "name": "竞品分析报告 - BrandX",
            "type": "竞品分析",
            "brand_id": 1,
            "date_range": "2026-03-01 ~ 2026-03-25",
            "created_at": "2026-03-25 14:00",
            "status": "ready"
        }
    ]
