from pydantic import BaseModel


class PingModel(BaseModel):
    db: float | None = None
    cache: float | None = None
