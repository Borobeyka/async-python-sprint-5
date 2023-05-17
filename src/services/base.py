import datetime
from typing import Any, Dict, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


def set_params(statement: Select, model: Type[ModelType], params: dict) -> Select:
    for key, value in params.items():
        statement = statement.where(getattr(model, key) == value)
    return statement


class BaseService():
    def __init__(self, db: AsyncSession, model: Type[ModelType] | None = None):
        self.db = db
        self.model = model

    async def get(
            self,
            is_one: bool = False,
            **kwargs: Dict[str, Any]
    ) -> Type[ModelType] | None:
        statement = select(self.model)
        statement = set_params(statement, self.model, kwargs)
        result = await self.db.execute(statement=statement)
        if is_one:
            return result.unique().scalar_one_or_none()
        else:
            return result.unique().scalars().all()

    async def create(self, *, obj_in: Type[SchemaType]) -> Type[ModelType]:
        obj_in_data = jsonable_encoder(
            obj_in,
            custom_encoder={datetime.datetime: lambda date: date}
        )
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            *,
            db_obj: Type[ModelType],
            obj_in: Type[SchemaType] | Dict[str, Any]
    ) -> Type[ModelType]:
        statement = (
            update(self.model).
            where(self.model.id == db_obj.id).
            values(obj_in.dict(exclude_unset=True)).
            returning(self.model)
        )
        await self.db.execute(statement=statement)
        await self.db.commit()
        return db_obj
