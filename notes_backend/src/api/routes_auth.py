from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, auth
from .database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# PUBLIC_INTERFACE
@router.post("/register", response_model=schemas.UserOut, responses={409: {"model": schemas.ErrorResponse}})
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check for existing
    user = auth.get_user_by_username(db, user_in.username)
    if user:
        raise HTTPException(status_code=409, detail="Username already registered")
    hashed = auth.get_password_hash(user_in.password)
    new_user = models.User(
        username=user_in.username,
        hashed_password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# PUBLIC_INTERFACE
@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT.
    """
    user = auth.authenticate_user(db, user_in.username, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.JWT_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
