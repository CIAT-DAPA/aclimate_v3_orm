# mng_soil.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngSoil(Base):
    __tablename__ = 'mng_soil'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('mng_country.id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('mng_crop.id'), nullable=False)
    name = Column(String(255), nullable=False)
    sort_order = Column(Integer, nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    crop = relationship("MngCrop", back_populates="soils")
    setups = relationship("MngSetup", back_populates="soil")
    country = relationship("MngCountry", back_populates="soils")