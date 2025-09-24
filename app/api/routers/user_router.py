"""
User API Router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import security
from db.session import get_db
from models.user_model import User as UserModel
from repositories.user_repository import UserRepository
from schemas import user_schema
from services.user_service import UserService

router = APIRouter()


@router.get("/")
def read_root():
    """
    Health check endpoint for the User microservice.
    """
    return {"service": "User Microservice is running"}


@router.post("/register", response_model=user_schema.User)
def register_user(
    user_in: user_schema.UserCreate,
    service: UserService = Depends()
):
    """
    Create a new user and a default profile.
    """
    return service.register_user(user_data=user_in)


@router.post("/token", response_model=user_schema.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Authenticate user and return a JWT access token.
    """
    repo = UserRepository(db)
    # OAuth2 form uses "username" for the email field
    user = repo.get_user_by_email(email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token")
def verify_token(current_user: UserModel = Depends(security.get_current_user)):
    """
    An internal endpoint for the API Gateway (NGINX) to verify a token.
    The `get_current_user` dependency handles all validation. If the token
    is invalid, it will raise a 401 HTTPException, which NGINX will
    interpret as an authentication failure.
    If the token is valid, this function will execute and return a 200 OK
    response, which NGINX will interpret as an authentication success.
    """
    return {"status": "ok", "user_id": current_user.id}


@router.get("/me", response_model=user_schema.User)
def read_users_me(current_user: UserModel = Depends(security.get_current_user)):
    """
    Get the profile for the currently authenticated user.
    """
    return current_user
