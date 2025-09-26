"""
User and Profile models with relationships and cascade behavior (sqlalchemy).
"""

import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class ExperienceLevel(enum.Enum):
    """
    Experience levels for user profiles.
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


CASCADE_BEHAVIOUR = "all, delete-orphan"


class User(Base):
    """
    User model representing application users.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile = relationship("Profile", back_populates="user",
                           uselist=False, cascade=CASCADE_BEHAVIOUR)


class Profile(Base):
    """
    Profile model representing user profiles.
    """
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    experience_level = Column(Enum(ExperienceLevel),
                              default=ExperienceLevel.BEGINNER)
    challenge_mode_active = Column(Boolean, default=False)
    user = relationship("User", back_populates="profile")
    disgusts = relationship(
        "Disgust", back_populates="profile", cascade=CASCADE_BEHAVIOUR)
    allergies = relationship(
        "Allergy", back_populates="profile", cascade=CASCADE_BEHAVIOUR)


class Disgust(Base):
    """
    Disgust model representing ingredients a user dislikes.
    """
    __tablename__ = "disgusts"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String, index=True, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    profile = relationship("Profile", back_populates="disgusts")


class Allergy(Base):
    """
    Allergy model representing ingredients a user is allergic to.
    """
    __tablename__ = "allergies"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String, index=True, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    profile = relationship("Profile", back_populates="allergies")
