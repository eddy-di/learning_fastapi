from database import TestingSessionLocal, engine, Base, TestingRUDSessionLocal
from sqlalchemy import MetaData, Table, text
import pytest
import uuid
from main import app, get_db
from models import Menu

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def override_get_db_for_rud():
    try:
        db = TestingRUDSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db_for_rud


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def setup_db():
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def teardown_and_setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# @pytest.fixture()
# def test_session():
    # session = TestingSessionLocal()
    # yield session
    # session.rollback()
    # session.close()
    
