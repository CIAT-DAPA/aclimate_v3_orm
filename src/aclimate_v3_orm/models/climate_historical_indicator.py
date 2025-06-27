from sqlalchemy import Column, BigInteger, Integer, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from ..database.base import Base
from ..enums import Period



class ClimateHistoricalIndicator(Base):
    __tablename__ = 'climate_historical_indicator'

    id = Column(BigInteger, primary_key=True)
    indicator_id = Column(Integer, ForeignKey('mng_indicators.id'), nullable=False)
    location_id = Column(BigInteger, ForeignKey('mng_location.id'), nullable=False)
    value = Column(Float, nullable=False)
    period = Column(Enum(Period), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)


    indicator = relationship("MngIndicator", back_populates="climate_historical_indicators")
    location = relationship("MngLocation", back_populates="climate_historical_indicators")