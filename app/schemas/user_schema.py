"""
User Schemas (pydantic models)
"""

from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

from models.user_model import ExperienceLevel

# -- Base Schemas --


class DisgustBase(BaseModel):
    """
    Base Schema for a user's disgust (ingredient they dislike).
    """
    ingredient_name: str


class AllergyBase(BaseModel):
    """
    Base Schema for a user's allergy (ingredient they are allergic to).
    """
    ingredient_name: str


class ProfileBase(BaseModel):
    """
    Base Schema for a user's profile, which includes their experience level and
    whether or not they want challenging recipes.
    """
    experience_level: Optional[ExperienceLevel] = ExperienceLevel.BEGINNER
    challenge_mode_active: Optional[bool] = False


# -- Creation Schemas --

class DisgustCreate(DisgustBase):
    """
    Schema for creating a new disgust entry.
    """


class AllergyCreate(AllergyBase):
    """
    Schema for creating a new allergy entry.
    """


class ProfileCreate(ProfileBase):
    """
    Schema for creating a new user profile.
    """


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    email: EmailStr
    password: str


# -- Response Schemas (for reading data) -

class Disgust(DisgustBase):
    """
    Schema for reading a user's disgust entry.
    """
    id: int
    profile_id: int

    model_config = ConfigDict(from_attributes=True)


class Allergy(AllergyBase):
    """
    Schema for reading a user's allergy entry.
    """
    id: int
    profile_id: int

    model_config = ConfigDict(from_attributes=True)


class Profile(ProfileBase):
    """
    Schema for reading a user's profile, including their disgusts and allergies.
    """
    id: int
    user_id: int
    disgusts: List[Disgust] = []
    allergies: List[Allergy] = []

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    """
    Schema for reading a user's basic information, including their profile.
    """
    id: int
    email: EmailStr
    profile: Optional[Profile] = None

    model_config = ConfigDict(from_attributes=True)


# -- Token Schema --

class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for data contained in the JWT token.
    """
    email: Optional[str] = None
