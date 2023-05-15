from sqlalchemy import Integer, Column, String

from db.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
