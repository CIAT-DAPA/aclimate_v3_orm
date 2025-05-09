from sqlalchemy import Column, BigInteger, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime, timezone

class MngLocation(Base):
    __tablename__ = 'mng_location'

    id = Column(BigInteger, primary_key=True)
    admin_2_id = Column(BigInteger, ForeignKey('mng_admin_2.id'), nullable=False)
    name = Column(String(255), nullable=False)
    ext_id = Column(String(255))
    origin = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    visible = Column(Boolean, default=True)

    admin_2 = relationship('MngAdmin2', back_populates='mng_location')
    climate_historical_daily = relationship("ClimateHistoricalDaily", back_populates="mng_location")
    climate_historical_monthly = relationship("ClimateHistoricalMonthly", back_populates="mng_location")
    climate_historical_climatology = relationship("ClimateHistoricalClimatology", back_populates="mng_location")
