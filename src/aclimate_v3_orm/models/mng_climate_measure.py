from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from aclimate_v3_orm.database.base import Base

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

    daily_measurements = relationship("ClimateHistoricalDaily", back_populates="measure")
    monthly_measurements = relationship("ClimateHistoricalMonthly", back_populates="measure")
    climatology_data = relationship("ClimateHistoricalClimatology", back_populates="measure")