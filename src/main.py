import time

from fastapi import Depends, FastAPI, status
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import files, users
from core.config import config
from db.db import get_session
from db.redis import redis_cli
from models.system import PingModel
from services.logger import logger

app = FastAPI(
    title=config.app_title,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(files.router, prefix="/api", tags=["Files"])


@app.get("/ping", tags=["System"], response_model=PingModel, status_code=status.HTTP_200_OK)
async def ping_services(db: AsyncSession = Depends(get_session)):
    logger.debug("Request to ping services")
    try:
        start = time.time()
        statement = select(1)
        await db.execute(statement=statement)
        postgres_response = time.time() - start
    except Exception as ex:
        logger.debug(f"Error while requesting to ping postgres, error - {ex}")
        postgres_response = None
    try:
        start = time.time()
        await redis_cli().get("nothing")
        redis_response = time.time() - start
    except Exception as ex:
        logger.debug(f"Error while requesting to ping redis, error - {ex}")
        redis_response = None

    return {
        "db": postgres_response,
        "cache": redis_response
    }
