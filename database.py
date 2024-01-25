import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# Load .env file
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

TestingRUDSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
