import json
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from db.redis import redis_cli
from models.db.tokens import TokenModel
from models.db.users import UserModel
from models.user import UserBase
from services.base import BaseService

oauth2_model = OAuth2PasswordBearer(tokenUrl="auth")


class UserService(BaseService):
    async def get_user_by_token(self, token: str) -> UserBase:
        from_redis = await redis_cli.get(token)
        if from_redis:
            return UserBase(**json.loads(from_redis).get("user"))
        statement = select(self.model).join(TokenModel).where(
            and_(
                TokenModel.token == token,
                TokenModel.expire > datetime.now()
            )
        )
        user = (await self.db.execute(statement=statement)).scalar_one_or_none()
        if not user:
            return
        return UserBase(**user.__dict__)


async def get_current_user(
    token: str = Depends(oauth2_model),
    db: AsyncSession = Depends(get_session)
) -> UserBase:
    user = await UserService(db, UserModel).get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user
