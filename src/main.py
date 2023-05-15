import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_redis_cache import FastApiRedisCache

from core.config import config
from api import users


app = FastAPI(
    title=config.app_title,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(users.router, prefix="/api", tags=["Users"])


@app.on_event("startup")
def startup():
    FastApiRedisCache().init(
        host_url=config.redis_dsn,
        prefix=f"{config.app_title}-cache",
        response_header=f"{config.app_title}-cache"
    )


if __name__ == "__main__":
    uvicorn.run(app, host=config.app_host, port=config.app_port)
