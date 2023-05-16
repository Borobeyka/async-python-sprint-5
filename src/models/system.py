

from typing import Optional
from pydantic import BaseModel


class PingModel(BaseModel):
    db: Optional[float] = None
    cache: Optional[float] = None
