from datetime import datetime
from pydantic import UUID4, BaseModel


class FileBase(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    path: str
    is_downloable: bool
