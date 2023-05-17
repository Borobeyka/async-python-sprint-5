from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
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

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="files")
