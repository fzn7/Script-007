from typing import List, Optional

from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str
    content: Optional[str] = None


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    files: List[File] = []

    class Config:
        orm_mode = True
