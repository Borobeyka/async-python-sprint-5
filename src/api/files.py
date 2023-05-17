from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile as FAUploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.db.files import FileModel
from models.files import FileBase
from models.user import UserBase, UserFiles
from services.files import FileService
from services.users import get_current_user

router = APIRouter()


@router.get("/files/download")
async def user_files(
    identifier: Optional[str] = None,
    path: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user: UserBase = Depends(get_current_user),
) -> FileResponse | File:
    return await FileService(db, FileModel).download(current_user, identifier, path)


@router.post("/upload")
async def user_files(
    path: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user: UserBase = Depends(get_current_user),
    file: FAUploadFile = File()
):
    return await FileService(db, FileModel).upload(path, file, current_user)


@router.get("/files", response_model=UserFiles, status_code=status.HTTP_200_OK)
async def user_files(
    db: AsyncSession = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    files = await FileService(db, FileModel).get(user_id=current_user.id)
    return UserFiles(
        user_id=current_user.id,
        files=[
            FileBase(**file.__dict__) for file in files
        ]
    )
