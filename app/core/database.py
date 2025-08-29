from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.core.config import settings

# Engine & Session
engine = create_engine(settings.database_url, echo=settings.debug)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
