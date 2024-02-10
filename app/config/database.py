from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.config.base import db_url

async_engine = create_async_engine(db_url)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=async_engine)

Base = declarative_base()


async def get_async_db():
    """
    Creates a database session and closes it after finishing,
    if exception comes out executes `rollback()` method and returns None.
    """

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if AsyncSessionLocal is None:
        raise Exception(
            'Database session manager `AsyncSessionLocal` is not initialized.'
        )

    try:
        db = AsyncSessionLocal()
        yield db
        db.commit()
    except Exception:
        await db.rollback()
    finally:
        db.close()


async def create_all(connection: AsyncConnection):
    await connection.run_sync(Base.metadata.create_all)


async def drop_all(connection: AsyncConnection):
    await connection.run_sync(Base.metadata.drop_all)
