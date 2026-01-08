import logging
from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService
from app.schemas.auth import Token
from app.core.security import verify_password, create_access_token


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # check existing user
    existing_user = UserService.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    # create non-existing user
    try:
        user = UserService.create_user(db, user_in)
        db.commit()
        logger.debug(f"Creating user with email: {user.email}")
        logger.info(f"User created with email: {user.email}")
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )


@router.post("/login", response_model=Token)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, login_data.username)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Invalid email or password"
        )
    access_token = create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
