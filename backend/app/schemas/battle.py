from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.battle import BattleStatus

class BattleBase(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    
class BattleCreate(BattleBase):
    pass

class BattleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BattleStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    winner_id: Optional[int] = None
    transaction_hash: Optional[str] = None

class BattleInDB(BattleBase):
    id: int
    status: BattleStatus
    winner_id: Optional[int] = None
    transaction_hash: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Battle(BattleInDB):
    pass

class BattleParticipantBase(BaseModel):
    battle_id: int
    soldier_id: int

class BattleParticipantCreate(BattleParticipantBase):
    pass

class BattleParticipantUpdate(BaseModel):
    votes: Optional[int] = None

class BattleParticipantInDB(BattleParticipantBase):
    id: int
    votes: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BattleParticipant(BattleParticipantInDB):
    pass

class BattleWithParticipants(Battle):
    participants: List[BattleParticipant] = []

class VoteRequest(BaseModel):
    participant_id: int 