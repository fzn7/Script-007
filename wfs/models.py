from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Lazy is workaround for async, use either "subquery" or "selectin"
    # More info: https://github.com/tiangolo/fastapi/pull/2331#issuecomment-801461215 and https://github.com/tiangolo/fastapi/pull/2331#issuecomment-807528963
    items = relationship("Item", back_populates="owner", lazy="subquery")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="files")
