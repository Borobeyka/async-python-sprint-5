from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.db.files import FileModel
from models.user import UserFiles
from services.base import BaseService
from services.users import get_current_user

router = APIRouter()


@router.get("/files", response_model=UserFiles)
async def user_files(
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user)
):
    files = await BaseService(db, FileModel).get(user_id=current_user.id)
    return UserFiles(
        user_id=current_user.id,
        files=[{
            UserFiles(**file) for file in files
        }]
    )
