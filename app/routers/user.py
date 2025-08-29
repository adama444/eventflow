from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.schemas.user import User
from app.schemas.user import UserCreateRequest, UserCreateResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserCreateResponse)
def create_user(request: UserCreateRequest, db: Session = Depends(get_db_session)):
    """User endpoint for new users registration"""
    user = User(name=request.name, email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserCreateResponse(id=user.id, name=user.name, email=user.email)
