from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    wallet_address: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    nonce: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class User(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    wallet_address: Optional[str] = None 