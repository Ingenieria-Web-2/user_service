import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base


class ExperienceLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


cascade_behavior = "all, delete-orphan"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile = relationship("Profile", back_populates="user",
                           uselist=False, cascade=cascade_behavior)


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    experience_level = Column(Enum(ExperienceLevel),
                              default=ExperienceLevel.BEGINNER)
    challenge_mode_active = Column(Boolean, default=False)
    user = relationship("User", back_populates="profile")
    disgusts = relationship(
        "Disgust", back_populates="profile", cascade=cascade_behavior)
    allergies = relationship(
        "Allergy", back_populates="profile", cascade=cascade_behavior)


class Disgust(Base):
    __tablename__ = "disgusts"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String, index=True, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    profile = relationship("Profile", back_populates="disgusts")


class Allergy(Base):
    __tablename__ = "allergies"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String, index=True, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    profile = relationship("Profile", back_populates="allergies")
