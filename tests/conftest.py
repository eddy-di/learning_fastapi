import asyncio
from typing import Generator, Iterator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.database import Base, async_engine, get_async_db
from app.main import app
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# unit tests


@pytest_asyncio.fixture(scope='function')
async def async_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture
async def async_client(async_session):
    def override_get_db() -> Iterator[AsyncSession]:
        """Utility function to wrap the database session in a generator.

        Yields:
            Iterator[AsyncSession]: An iterator containing one database session.
        """
        yield async_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(
            app=app,
            base_url='http://test'
    ) as client:
        yield client

# scenario


@pytest_asyncio.fixture(scope='module')
async def scenario_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture
async def scenario_client(scenario_session):
    def override_get_db() -> Iterator[AsyncSession]:
        """Utility function to wrap the database session in a generator.

        Yields:
            Iterator[AsyncSession]: An iterator containing one database session.
        """
        yield scenario_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(
            app=app,
            base_url='http://test'
    ) as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def create_menu(async_session: AsyncSession):
    db_menu_item = Menu(
        title='testMenu1',
        description='testMenu1Description'
    )
    async_session.add(db_menu_item)
    await async_session.commit()
    await async_session.refresh(db_menu_item)
    await async_session.close()
    return db_menu_item


@pytest_asyncio.fixture(scope='function')
async def create_submenu(async_session: AsyncSession):
    async def make_menu(menu_id):
        db_submenu_item = SubMenu(
            title='testSubMenu1',
            description='testSubMenu1Description',
            menu_id=menu_id
        )
        async_session.add(db_submenu_item)
        await async_session.commit()
        await async_session.refresh(db_submenu_item)
        await async_session.close()
        return db_submenu_item
    return make_menu


@pytest_asyncio.fixture(scope='function')
async def create_dish(async_session: AsyncSession):
    async def make_dish(submenu_id):
        db_dish_item = Dish(
            title='testDishTitle1',
            description='testDishDescription1',
            price='11.10',
            submenu_id=submenu_id
        )
        async_session.add(db_dish_item)
        await async_session.commit()
        await async_session.refresh(db_dish_item)
        await async_session.close()
        return db_dish_item
    return make_dish
