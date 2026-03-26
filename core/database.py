"""
数据库连接与初始化
使用 Supabase PostgreSQL
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def init_db():
    """初始化数据库表（创建 MiraSeek 专用表）"""
    # SQL 语句通过 Supabase 执行
    # 由于 Supabase Python SDK 不直接支持 DDL，这里只是占位
    # 实际表创建需要通过 Supabase Dashboard 的 SQL Editor 执行
    print("✅ Database connection established")
    print("📋 Please run the SQL migration in Supabase Dashboard")
    pass


def get_supabase() -> Client:
    """获取 Supabase 客户端"""
    return supabase
