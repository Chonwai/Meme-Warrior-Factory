from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MemeSoldierBase(BaseModel):
    name: str
    prompt: str

class MemeSoldierCreate(MemeSoldierBase):
    pass

class MemeSoldierUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    coin_icon_url: Optional[str] = None
    token_id: Optional[str] = None
    contract_address: Optional[str] = None
    deployed_to_battlefield: Optional[bool] = None
    token_amount: Optional[float] = None
    token_amount_deployed: Optional[float] = None

class MemeSoldierInDB(MemeSoldierBase):
    id: int
    owner_id: int
    image_url: Optional[str] = None
    token_id: Optional[str] = None
    contract_address: Optional[str] = None
    coin_icon_url: Optional[str] = None
    deployed_to_battlefield: bool
    token_amount: float = 0.0
    token_amount_deployed: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class MemeSoldier(MemeSoldierInDB):
    pass

class MemeSoldierGeneration(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500)

class MemeSoldierGenerationResponse(BaseModel):
    id: int
    name: str
    image_url: str
    prompt: str
    coin_icon_url: Optional[str] = None 