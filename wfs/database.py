import databases

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///db/wfs.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(SQLALCHEMY_DATABASE_URL)
await database.connect()

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False} # check_same_thread -> sqlite only
)

Base = declarative_base()
