import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash, generate_password_hash

from core.config import config
from db.db import get_session
from db.redis import redis_cli
from models.db.tokens import TokenModel
from models.db.users import UserModel
from models.user import UserBase, UserLoginOrRegister, UserToken
from services.base import BaseService
from services.users import get_current_user

router = APIRouter()


@router.post(
    "/register",
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED,
    description="Registration user"
)
async def user_register(user: UserLoginOrRegister, db: AsyncSession = Depends(get_session)):
    user.password = generate_password_hash(user.password)
    answer = await BaseService(db, UserModel).create(obj_in=user)
    return UserBase(**answer.__dict__)


@router.post(
    "/auth",
    response_model=UserToken,
    status_code=status.HTTP_201_CREATED,
    description="Authentication user"
)
async def user_auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    user = await BaseService(db, UserModel).get(is_one=True, username=form_data.username)
    if not user or not check_password_hash(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong username or password"
        )
    token = await BaseService(db, TokenModel).create(obj_in={
        "user_id": user.id,
        "expire": datetime.now() + config.token_expire
    })
    async with redis_cli().pipeline(transaction=True) as pipe:
        await pipe.set(
            str(token.token),
            json.dumps({
                "expires": token.expire.timestamp(),
                "user": UserBase(**user.__dict__).__dict__
            }),
            ex=config.redis_expire
        ).execute()
    return UserToken(**token.__dict__)


@router.get("/me", response_model=UserBase, description="Get info of authenticated user")
async def me(current_user: UserBase = Depends(get_current_user)) -> UserBase:
    return current_user
