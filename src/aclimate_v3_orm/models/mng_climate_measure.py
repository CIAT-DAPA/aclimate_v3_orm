from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base

class MngClimateMeasure(Base):
    __tablename__ = 'mng_climate_measure'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    short_name = Column(String(75), nullable=False)
    unit = Column(String(50), nullable=False)
    description = Column(Text)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


    climate_historical_daily = relationship("ClimateHistoricalDaily", back_populates="mng_climate_measureasure")
    climate_historical_monthly = relationship("ClimateHistoricalMonthly", back_populates="mng_climate_measure")
    climate_historical_climatology = relationship("ClimateHistoricalClimatology", back_populates="mng_climate_measure")