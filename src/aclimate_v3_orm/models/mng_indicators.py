from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.base import Base
from ..enums import IndicatorsType


class MngIndicator(Base):
    __tablename__ = 'mng_indicators'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(IndicatorsType), nullable=False)
    name = Column(String(150), nullable=False)
    short_name = Column(String(50), nullable=False)
    unit = Column(String(25), nullable=False)
    description = Column(Text)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    climate_historical_indicators = relationship(
        "ClimateHistoricalIndicator", 
        back_populates="indicator",
        cascade="all, delete-orphan"
    )