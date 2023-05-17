from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import config

Base = declarative_base()

engine = create_async_engine(
    config.postgres_dsn,
    echo=config.app_query_logging,
    future=True
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
