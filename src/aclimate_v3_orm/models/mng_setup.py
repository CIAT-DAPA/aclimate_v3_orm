# mng_setup.py
from sqlalchemy import Column, BigInteger, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngSetup(Base):
    __tablename__ = 'mng_setup'

    id = Column(BigInteger, primary_key=True)
    cultivar_id = Column(Integer, ForeignKey('mng_cultivar.id'), nullable=False)
    soil_id = Column(Integer, ForeignKey('mng_soil.id'), nullable=False)
    season_id = Column(BigInteger, ForeignKey('season.id'), nullable=False)
    frequency = Column(Integer, nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    cultivar = relationship("MngCultivar", back_populates="setups")
    soil = relationship("MngSoil", back_populates="setups")
    season = relationship("Season", back_populates="setups")

    configuration_files = relationship("MngConfigurationFile", back_populates="setup")