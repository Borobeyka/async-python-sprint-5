from uuid import uuid4
from sqlalchemy import DateTime, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from db.db import Base


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(
        UUIDType(binary=False),
        unique=True,
        default=uuid4
    )
    expire = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="tokens")
