from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime
from .base import PaperBase, ConferenceBase
from app.models.user import RoleType

class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    role: Optional[RoleType] = None

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v[0].isalpha() or not v.replace('_', '').isalnum() or len(v) < 5:
            raise ValueError('To Onoma xristi tha prepei na 3ekinaei me gramma, na einai toulaxiston 5 xaraktirwn kai na periexei mono alfarithmitika kai katw paula')
        return v

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError('O kwdikos prepei na exei mikos toulaxiston 8 grammatwn')
        if not any(char.isupper() for char in v):
            raise ValueError('O kwdikos tha prepei na periexei toulaxiston ena kefalaio')
        if not any(char.islower() for char in v):
            raise ValueError('O kwdikos tha prepei na periexei toulaxiston ena pezo')
        if not any(char.isdigit() for char in v):
            raise ValueError('O kwdikos tha prepei na periexei toulaxiston ena psifio')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in v):
            raise ValueError('O kwdikos tha prepei na periexei enan toulaxiston eidiko xaraktira')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if v is not None:
            if not v[0].isalpha() or not v.replace('_', '').isalnum() or len(v) < 5:
                raise ValueError('To Onoma xristi tha prepei na 3ekinaei me gramma, na einai toulaxiston 5 xaraktirwn kai na periexei mono alfarithmitika kai katw paula')
        return v

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError('O kwdikos prepei na exei mikos toulaxiston 8 grammatwn')
        if not any(char.isupper() for char in v):
            raise ValueError('O kwdikos tha prepei na periexei toulaxiston ena kefalaio')
        if not any(char.islower() for char in v):
            raise ValueError('O kwdikos tha prepei na periexei toulaxiston ena pezo')
        if not any(char.isdigit() for char in v):
            raise ValueError('O kwdikos tha prepei na periexei toulaxiston ena psifio')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in v):
            raise ValueError('O kwdikos tha prepei na periexei enan toulaxiston eidiko xaraktira')
        return v

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    role: RoleType
    authored_papers: List[PaperBase] = []
    chaired_conferences: List[ConferenceBase] = []
    pc_member_conferences: List[ConferenceBase] = []
    reviewed_papers: List[PaperBase] = []
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserInDB(User):
    hashed_password: str
    failed_login_attempts: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
