from typing import List

from fastapi import Depends, FastAPI, HTTPException

from . import crud, models, schemas
from .database import Base, engine

from sqlalchemy.ext.asyncio import AsyncSession

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def start_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_db():
    session = AsyncSession(engine, expire_on_commit=True)
    try:
        yield session
    finally:
        await session.close()


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/files/", response_model=schemas.File)
async def create_file_for_user(
    user_id: int, file: schemas.FileCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_user_file(db=db, file=file, user_id=user_id)


@app.get("/items/", response_model=List[schemas.File])
async def read_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_files(db, skip=skip, limit=limit)
