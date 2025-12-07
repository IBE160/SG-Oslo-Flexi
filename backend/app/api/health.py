from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from redis import Redis
from app.db.session import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health/db")
async def health_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            return {"status": "connected"}
        else:
            raise HTTPException(status_code=503, detail="Database query failed")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@router.get("/health/redis")
def health_redis():
    try:
        redis_conn = Redis.from_url(settings.REDIS_URL)
        if redis_conn.ping():
             return {"status": "connected"}
        else:
             raise HTTPException(status_code=503, detail="Redis ping failed")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis connection failed: {str(e)}")
