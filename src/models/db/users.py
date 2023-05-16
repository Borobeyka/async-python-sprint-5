from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from db.db import Base
from models.db.files import FileModel # noqa F401


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(128))

    files = relationship("FileModel", back_populates="user", passive_deletes=True)
    tokens = relationship("TokenModel", back_populates="user", passive_deletes=True)
