from datetime import datetime
from io import BytesIO
import os
from typing import Optional
from zipfile import ZipFile
import aiofiles
from pathlib import Path
from fastapi import File, HTTPException, status, UploadFile as FAUploadFile
from fastapi.responses import StreamingResponse, FileResponse
from models.files import FileUpload, FileUploadResponse
from models.user import UserBase
from services.base import BaseService

from core.config import config


class FileService(BaseService):
    async def upload(
        self,
        path: Optional[str],
        file: FAUploadFile,
        user: UserBase
    ) -> FileUploadResponse:
        path = f"{path}/" if path else ""
        upload_file = await self.create(obj_in=FileUpload(
            name=file.filename,
            path=f"{path}{file.filename}",
            size=len(await file.read()),
            user_id=user.id
        ))
        file.file.seek(0)
        content = file.file.read()
        directory = f"{config.folder_upload}/{user.username}/{path}"
        p = Path(directory)
        try:
            if not Path.exists(p):
                Path(p).mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(Path(p, file.filename), "wb") as f:
                await f.write(content)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File not saved"
            )
        return FileUploadResponse(**upload_file.__dict__)

    async def download(
        self,
        user: UserBase,
        identifier: Optional[str] = None,
        path: Optional[str] = None
    ):
        if path:
            directory = f"{config.folder_upload}/{user.username}/{path}"
            directory_files = [
                f"{directory}/{file.name}" for file in list(Path(directory).iterdir())
            ]
            return self.zip_folder(directory_files)
        if identifier:
            file = await self.get(is_one=True, id=identifier)
            file_path = f"{config.folder_upload}/{user.username}/{file.path}"
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return FileResponse(
                    path=file_path,
                    filename=file.name,
                    media_type="application/octet-stream"
                )

    def zip_folder(self, file_list: list) -> File:
        io = BytesIO()
        zip_name = f"{str(datetime.now())}.zip"
        with ZipFile(io, "w") as zip:
            for file in file_list:
                zip.write(file)
        return StreamingResponse(
            iter([io.getvalue()]),
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment filename={zip_name}"}
        )
