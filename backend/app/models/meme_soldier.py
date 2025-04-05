from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class MemeSoldier(Base):
    __tablename__ = "meme_soldiers"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    token_id = Column(String, index=True)  # Blockchain token ID
    name = Column(String, index=True)
    image_url = Column(String)
    prompt = Column(Text)
    
    # Blockchain info
    contract_address = Column(String)
    coin_icon_url = Column(String)  # URL to the meme soldier's coin icon
    deployed_to_battlefield = Column(Boolean, default=False)
    token_amount = Column(Float)  # Total token amount
    token_amount_deployed = Column(Float)  # Amount in battlefield
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="soldiers")
    battle_participations = relationship("BattleParticipant", back_populates="soldier") 