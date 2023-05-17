from datetime import datetime

from pydantic import UUID4, BaseModel


class FileBase(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool


class FileUpload(BaseModel):
    name: str
    path: str
    size: int
    user_id: int


class FileUploadResponse(FileBase):
    NotImplemented
