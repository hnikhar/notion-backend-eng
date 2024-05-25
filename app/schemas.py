from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from typing import Optional
from app.models import LeadState

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    resume: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    state: LeadState

class Lead(LeadBase):
    id: int
    state: LeadState

    class Config:
        orm_mode = True
        use_enum_values = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str
