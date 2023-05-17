from datetime import datetime
from typing import List

from pydantic import UUID4, BaseModel, Field, validator

from models.files import FileBase


class BaseWithORM(BaseModel):
    username: str

    class Config:
        orm_model = True


class UserBase(BaseWithORM):
    id: int


class UserLoginOrRegister(BaseWithORM):
    password: str


class UserToken(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expire: datetime
    token_type: str | None = "bearer"

    class Config:
        orm_model = True
        allow_population_by_field_name = True

        @validator("token")
        def token_to_str(cls, value):
            return str(value)


class UserFiles(BaseModel):
    user_id: int
    files: List[FileBase]
