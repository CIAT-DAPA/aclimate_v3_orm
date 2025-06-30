from sqlalchemy import Column, BigInteger, String, Float, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngLocation(Base):
    __tablename__ = 'mng_location'

    id = Column(BigInteger, primary_key=True)
    admin_2_id = Column(BigInteger, ForeignKey('mng_admin_2.id'), nullable=False)
    source_id = Column(Integer, ForeignKey('mng_source.id'), nullable=False)
    name = Column(String(255), nullable=False)
    ext_id = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    visible = Column(Boolean, default=True)


    admin_2 = relationship('MngAdmin2', back_populates='location')
    source = relationship('MngSource', back_populates='location')
    
    daily_measurements = relationship("ClimateHistoricalDaily", back_populates="location")
    monthly_measurements = relationship("ClimateHistoricalMonthly", back_populates="location")
    climatology_data = relationship("ClimateHistoricalClimatology", back_populates="location")
    climate_historical_indicators = relationship('ClimateHistoricalIndicator', back_populates='location')
    #setups = relationship("MngSetup", back_populates="location")
    seasons = relationship("Season", back_populates="location")
