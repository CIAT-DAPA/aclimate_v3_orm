# mng_crop.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngCrop(Base):
    __tablename__ = 'mng_crop'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    soils = relationship("MngSoil", back_populates="crop")
    cultivars = relationship("MngCultivar", back_populates="crop")
    stages = relationship("MngPhenologicalStage", back_populates="crop")
    seasons = relationship("Season", back_populates="crop")