from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config.base import db_url

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session | None:
    """
    Creates a database session and closes it after finishing,
    if exception comes out executes `rollback()` method and returns None.
    """

    try:
        db = SessionLocal()
        yield db
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
