from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserCreateRequest(BaseModel):
    name: str
    email: str


class UserCreateResponse(BaseModel):
    id: int
    name: str
    email: str


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
