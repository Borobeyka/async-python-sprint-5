from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.db.users import UserModel
from models.user import UserBase
from services.base import BaseService


oauth2_model = OAuth2PasswordBearer(tokenUrl="auth")


async def get_current_user(
    token: str = Depends(oauth2_model),
    db: AsyncSession = Depends(get_session)
) -> UserBase:
    user = await BaseService(db, UserModel).get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user
