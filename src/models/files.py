from uuid import uuid4
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Column, String
from sqlalchemy_utils import UUIDType

from db.db import Base


class FileModel(Base):
    __tablename__ = "files"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    name = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)
    path = Column(String(256))
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
    author_id = Column(ForeignKey("users.id"))
