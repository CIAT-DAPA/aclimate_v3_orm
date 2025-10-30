from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.base import Base
from ..enums import IndicatorsType, Period


class MngIndicator(Base):
    __tablename__ = 'mng_indicators'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(IndicatorsType), nullable=False)
    name = Column(String(150), nullable=False)
    short_name = Column(String(50), nullable=False)
    unit = Column(String(25), nullable=False)
    temporality = Column(Enum(Period), nullable=False)
    description = Column(Text)
    indicator_category_id = Column(Integer, ForeignKey('mng_indicator_category.id'), nullable=True)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    climate_historical_indicators = relationship(
        "ClimateHistoricalIndicator", 
        back_populates="indicator",
        cascade="all, delete-orphan"
    )

    historical_agroclimatic_indicators = relationship(
        "HistoricalAgroclimaticIndicator", back_populates="indicator"
    )
    country_indicators = relationship('MngCountryIndicator', back_populates='indicator', cascade="all, delete-orphan")
    category = relationship('MngIndicatorCategory', back_populates='indicators')