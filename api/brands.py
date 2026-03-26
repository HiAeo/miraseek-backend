"""
品牌管理 API
"""
from fastapi import APIRouter, HTTPException
from typing import List
from core.database import get_supabase
from models.schemas import Brand, BrandCreate

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_brands():
    """获取所有品牌"""
    supabase = get_supabase()
    result = supabase.table("miraseek_brands").select("*").execute()
    return result.data


@router.post("/")
async def create_brand(brand: BrandCreate):
    """创建品牌"""
    supabase = get_supabase()
    data = brand.model_dump()
    result = supabase.table("miraseek_brands").insert(data).execute()
    return {"code": 0, "message": "success", "data": result.data[0]}


@router.get("/{brand_id}")
async def get_brand(brand_id: int):
    """获取单个品牌"""
    supabase = get_supabase()
    result = supabase.table("miraseek_brands").select("*").eq("id", brand_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"code": 0, "data": result.data[0]}


@router.put("/{brand_id}")
async def update_brand(brand_id: int, brand: BrandCreate):
    """更新品牌"""
    supabase = get_supabase()
    data = brand.model_dump()
    result = supabase.table("miraseek_brands").update(data).eq("id", brand_id).execute()
    return {"code": 0, "message": "success", "data": result.data[0]}


@router.delete("/{brand_id}")
async def delete_brand(brand_id: int):
    """删除品牌"""
    supabase = get_supabase()
    supabase.table("miraseek_brands").delete().eq("id", brand_id).execute()
    return {"code": 0, "message": "success"}
