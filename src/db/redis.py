import redis.asyncio as redis

from core.config import config


async def redis_cli():
    return await redis.from_url(config.redis_dsn)
