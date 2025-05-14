from sqlalchemy import Column, BigInteger, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class ClimateHistoricalClimatology(Base):
    __tablename__ = 'climate_historical_climatology'

    id = Column(BigInteger, primary_key=True)
    location_id = Column(BigInteger, ForeignKey("mng_location.id"), nullable=False)
    measure_id = Column(Integer, ForeignKey("mng_climate_measure.id"), nullable=False)
    month = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)

    location = relationship("MngLocation", back_populates="climatology_data")
    measure = relationship("MngClimateMeasure", back_populates="climatology_data")