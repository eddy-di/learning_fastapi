from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.base import db_url

async_engine = create_async_engine(db_url)

AsyncSessionLocal = sessionmaker(autoflush=False, autocommit=False, class_=AsyncSession,
                                 expire_on_commit=False, bind=async_engine)

Base = declarative_base()


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_db():
    # """
    # Creates a database session and closes it after finishing,
    # """

    # if AsyncSessionLocal is None:
    # raise Exception(
    # 'Database session manager `AsyncSessionLocal` is not initialized.'
    # )

    async with AsyncSessionLocal() as session:
        yield session

    # try:
        # db = AsyncSessionLocal()
        # yield db
        # await db.commit()
    # except Exception:
        # await db.rollback()
    # finally:
        # await db.close()

# for tests


async def create_all(connection: AsyncConnection):
    await connection.run_sync(Base.metadata.create_all)


async def drop_all(connection: AsyncConnection):
    await connection.run_sync(Base.metadata.drop_all)
