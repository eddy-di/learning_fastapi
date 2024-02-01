from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import db_url


engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

