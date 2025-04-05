from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.config.database import Base

class BattleStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Battle(Base):
    __tablename__ = "battles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    status = Column(Enum(BattleStatus), default=BattleStatus.PENDING)
    
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    
    winner_id = Column(Integer, ForeignKey("battle_participants.id"), nullable=True)
    transaction_hash = Column(String, nullable=True)  # Blockchain transaction hash
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    participants = relationship("BattleParticipant", back_populates="battle", foreign_keys="BattleParticipant.battle_id")
    winner = relationship("BattleParticipant", foreign_keys=[winner_id])

class BattleParticipant(Base):
    __tablename__ = "battle_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    battle_id = Column(Integer, ForeignKey("battles.id"))
    soldier_id = Column(Integer, ForeignKey("meme_soldiers.id"))
    
    votes = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    battle = relationship("Battle", back_populates="participants", foreign_keys=[battle_id])
    soldier = relationship("MemeSoldier", back_populates="battle_participations") 