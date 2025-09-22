from typing import Optional

from sqlalchemy.orm import Session

from core.security import hash_password
from models.user_model import Profile, User
from schemas.user_schema import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate) -> User:
        hashed_pass = hash_password(user.password)
        db_user = User(email=user.email, hashed_password=hashed_pass)
        # Create a default profile for the new user
        db_profile = Profile()
        db_user.profile = db_profile
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
