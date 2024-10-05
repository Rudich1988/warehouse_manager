from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from warehous_manager.config.base import Config


class ModelBase(DeclarativeBase):
    pass


engine = create_async_engine(Config.DATABASE_URL, echo=True)
Session = async_sessionmaker(bind=engine)

@asynccontextmanager
async def db_session():
    session = Session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
