import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, engine, generate_uuid
from models import Menu, SubMenu, Dish


from main import app, get_db

@pytest.fixture
def init_db():
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def drop_db():
    Base.metadata.drop_all(bind=engine)


TEST_DB_URL = 'sqlite:///./test_sqlite_db.sqlite3'
SQLALCHEMY_DATABASE_URL = TEST_DB_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

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
    test_client = TestClient(app)
    yield test_client
    # drop test_db after tests
    Base.metadata.drop_all(bind=engine)

# 
def create_menu(id: str):
    session = TestingSessionLocal()
    db_menu_item = Menu(
        id=id,
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    session.refresh(db_menu_item)


def create_submenu(menu_id, submenu_id):
    session = TestingSessionLocal()
    db_menu_item = Menu(
        id=menu_id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    db_submenu_item = SubMenu(
        id=submenu_id,
        title='testSubMenu1',
        description='testSubMenu1Description',
        menu_id=db_menu_item.id
    )
    session.add(db_submenu_item)
    session.commit()
    session.close()


def create_dish(menu_id, submenu_id, dish_id):
    session = TestingSessionLocal()
    db_menu_item = Menu(
        id=menu_id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    db_submenu_item = SubMenu(
        id=submenu_id,
        title='testSubMenu1',
        description='testSubMenu1Description',
        menu_id=db_menu_item.id
    )
    session.add(db_submenu_item)
    session.commit()
    db_dish_item = Dish(
        id=dish_id,
        title='testDishTitle1',
        description='testDishDescription1',
        price='11.10',
        submenu_id=db_submenu_item.id
    )
    session.add(db_dish_item)
    session.commit()
    session.close()