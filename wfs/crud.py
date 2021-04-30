import hashlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, fs, config, utils


async def get_user(db: AsyncSession, user_id: int):
    db_execute = await db.execute(select(models.User).where(models.User.id == user_id))
    user = db_execute.scalars().first()

    for file in user.files:
        if file.filepath:
            file.content = fs.read(config.STORAGE_DIR, file.filepath)

    return user


async def get_user_by_email(db: AsyncSession, email: str):
    db_execute = await db.execute(select(models.User).where(models.User.email == email))
    return db_execute.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(models.User).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = hashlib.sha512(
        (user.password +
         config.ENCRYPTION_KEY +
         config.SALT).encode(
            config.DEFAULT_ENCODING)).hexdigest()
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_files(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(models.File).offset(skip).limit(limit))
    files = db_execute.scalars().all()

    for file in files:
        if file.filepath:
            file.content = fs.read(config.STORAGE_DIR, file.filepath)

    return files


async def create_user_file(db: AsyncSession, file: schemas.FileCreate, user_id: int):
    filepath = utils.generate_string(config.FILENAME_LENGTH)
    fs.create(config.STORAGE_DIR, filepath, file.content)

    db_file = models.File(
        filename=file.filename,
        filepath=filepath,
        owner_id=user_id)
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)

    db_file.content = file.content

    return db_file
