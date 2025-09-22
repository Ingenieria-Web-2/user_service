from typing import List, Optional

from pydantic import BaseModel, EmailStr

from models.user_model import ExperienceLevel

# -- Base Schemas --


class DisgustBase(BaseModel):
    ingredient_name: str


class AllergyBase(BaseModel):
    ingredient_name: str


class ProfileBase(BaseModel):
    experience_level: Optional[ExperienceLevel] = ExperienceLevel.BEGINNER
    challenge_mode_active: Optional[bool] = False
# -- Creation Schemas --


class DisgustCreate(DisgustBase):
    pass


class AllergyCreate(AllergyBase):
    pass


class ProfileCreate(ProfileBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str
# -- Response Schemas (for reading data) --


class Disgust(DisgustBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True


class Allergy(AllergyBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True


class Profile(ProfileBase):
    id: int
    user_id: int
    disgusts: List[Disgust] = []
    allergies: List[Allergy] = []

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    email: EmailStr
    profile: Optional[Profile] = None

    class Config:
        from_attributes = True
# -- Token Schema --


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
