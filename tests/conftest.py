import pytest
from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.base import db_url
from app.config.cache import create_redis as redis
from app.config.database import Base, get_db
from app.main import app
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu

engine = create_engine(db_url)


@pytest.fixture
def init_db():
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def drop_db():
    Base.metadata.drop_all(bind=engine)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the database dependency for testing


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture
def setup_test_db():
    # creates db and drops it at the end
    Base.metadata.create_all(bind=engine)
    r = redis()
    test_client = TestClient(app)
    yield test_client
    # drop test_db after tests
    Base.metadata.drop_all(bind=engine)
    r.flushdb()


@pytest.fixture
def cache_connect() -> Redis:
    return redis()


@pytest.fixture
def cache_flush():
    return redis().flushdb()


@pytest.fixture
def create_menu():
    session = TestingSessionLocal()
    db_menu_item = Menu(
        title='testMenu1',
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    session.refresh(db_menu_item)
    session.close()
    return db_menu_item


@pytest.fixture
def create_submenu():
    def make_menu(menu_id):
        session = TestingSessionLocal()
        db_submenu_item = SubMenu(
            title='testSubMenu1',
            description='testSubMenu1Description',
            menu_id=menu_id
        )
        session.add(db_submenu_item)
        session.commit()
        session.refresh(db_submenu_item)
        session.close()
        return db_submenu_item
    return make_menu


@pytest.fixture
def create_dish():
    def make_dish(submenu_id):
        session = TestingSessionLocal()
        db_dish_item = Dish(
            title='testDishTitle1',
            description='testDishDescription1',
            price='11.10',
            submenu_id=submenu_id
        )
        session.add(db_dish_item)
        session.commit()
        session.refresh(db_dish_item)
        session.close()
        return db_dish_item
    return make_dish
