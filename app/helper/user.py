from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.user import User


def create_user(db: Session, name: str, email: str) -> User:
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt).scalar_one_or_none()
    return result
