from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session

router = APIRouter()


@router.get("/ping")
async def ping_services(db: AsyncSession = Depends(get_session)):
    ...
