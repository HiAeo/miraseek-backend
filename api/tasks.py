"""
监控任务 API
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from core.database import get_supabase
from models.schemas import Task, TaskCreate

router = APIRouter()


@router.get("/")
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    brand_id: Optional[int] = None,
    status: Optional[str] = None
):
    """获取监控任务列表"""
    supabase = get_supabase()
    query = supabase.table("miraseek_tasks").select("*, miraseek_brands(brand_name)")
    
    if brand_id:
        query = query.eq("brand_id", brand_id)
    if status:
        query = query.eq("is_active", status == "active")
    
    result = query.range(skip, skip + limit - 1).execute()
    
    # 格式化返回数据
    tasks = []
    for item in result.data:
        task = {
            "id": item["id"],
            "brand_id": item["brand_id"],
            "brand_name": item.get("miraseek_brands", {}).get("brand_name", ""),
            "prompt_text": item["prompt_text"],
            "prompt_type": item["prompt_type"],
            "ai_models": item["ai_models"],
            "frequency": item["frequency"],
            "is_active": item["is_active"],
            "created_at": item["created_at"]
        }
        tasks.append(task)
    
    return {"code": 0, "data": {"total": len(tasks), "items": tasks}}


@router.post("/")
async def create_task(task: TaskCreate):
    """创建监控任务"""
    supabase = get_supabase()
    data = task.model_dump()
    result = supabase.table("miraseek_tasks").insert(data).execute()
    return {"code": 0, "message": "success", "data": result.data[0]}


@router.get("/{task_id}")
async def get_task(task_id: int):
    """获取单个任务"""
    supabase = get_supabase()
    result = supabase.table("miraseek_tasks").select("*").eq("id", task_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"code": 0, "data": result.data[0]}


@router.put("/{task_id}")
async def update_task(task_id: int, task: TaskCreate):
    """更新任务"""
    supabase = get_supabase()
    data = task.model_dump()
    result = supabase.table("miraseek_tasks").update(data).eq("id", task_id).execute()
    return {"code": 0, "message": "success", "data": result.data[0]}


@router.put("/{task_id}/toggle")
async def toggle_task(task_id: int):
    """切换任务状态（启用/暂停）"""
    supabase = get_supabase()
    # 先获取当前状态
    result = supabase.table("miraseek_tasks").select("is_active").eq("id", task_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_status = not result.data[0]["is_active"]
    supabase.table("miraseek_tasks").update({"is_active": new_status}).eq("id", task_id).execute()
    return {"code": 0, "message": "success", "data": {"is_active": new_status}}


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    """删除任务"""
    supabase = get_supabase()
    supabase.table("miraseek_tasks").delete().eq("id", task_id).execute()
    return {"code": 0, "message": "success"}
