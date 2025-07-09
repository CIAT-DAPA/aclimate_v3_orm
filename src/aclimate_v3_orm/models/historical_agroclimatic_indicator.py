from sqlalchemy import Column, BigInteger, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class HistoricalAgroclimaticIndicator(Base):
    __tablename__ = 'historical_agroclimatic_indicator'

    id = Column(BigInteger, primary_key=True)
    indicator_id = Column(Integer, ForeignKey('mng_indicators.id'), nullable=False)
    location_id = Column(BigInteger, ForeignKey('mng_location.id'), nullable=False)
    phenological_id = Column(Integer, ForeignKey('mng_phenological_stage.id'), nullable=False)
    value = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    indicator = relationship("MngIndicator", back_populates="historical_agroclimatic_indicators")
    location = relationship("MngLocation", back_populates="historical_agroclimatic_indicators")
    phenological_stage = relationship("MngPhenologicalStage", back_populates="historical_agroclimatic_indicators")