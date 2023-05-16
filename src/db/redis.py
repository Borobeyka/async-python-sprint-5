import redis

from core.config import config

redis_cli = redis.Redis(host=config.redis_host, port=config.redis_port)
