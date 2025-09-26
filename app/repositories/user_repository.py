"""
Repository for user-related database operations.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user_model import Profile, User
from app.schemas.user_schema import UserCreate


class UserRepository:
    """
    Repository for user-related database operations.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.
        """
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate) -> User:
        """
        Create a new user with a hashed password and a default profile.
        """
        hashed_pass = hash_password(user.password)
        db_user = User(email=user.email, hashed_password=hashed_pass)
        # Create a default profile for the new user
        db_profile = Profile()
        db_user.profile = db_profile
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
