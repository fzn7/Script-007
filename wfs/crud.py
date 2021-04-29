import hashlib
from sqlalchemy.orm import Session
from . import models, schemas, fs, config, utils


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    for file in user.files:
        if file.filepath:
            file.content = fs.read(config.STORAGE_DIR, file.filepath)

    return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashlib.sha512(
        (user.password +
         config.ENCRYPTION_KEY +
         config.SALT).encode(
            config.DEFAULT_ENCODING)).hexdigest()
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_files(db: Session, skip: int = 0, limit: int = 100):
    files = db.query(models.File).offset(skip).limit(limit).all()

    print(files)

    for file in files:
        if file.filepath:
            file.content = fs.read(config.STORAGE_DIR, file.filepath)

    return files


def create_user_file(db: Session, file: schemas.FileCreate, user_id: int):
    filepath = utils.generate_string(config.FILENAME_LENGTH)
    fs.create(config.STORAGE_DIR, filepath, file.content)

    db_file = models.File(
        filename=file.filename,
        filepath=filepath,
        owner_id=user_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    db_file.content = file.content

    return db_file
