from sqlalchemy import Column, BigInteger, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class ClimateHistoricalDaily(Base):
    __tablename__ = 'climate_historical_daily'

    id = Column(BigInteger, primary_key=True)
    location_id = Column(BigInteger, ForeignKey("admin_location.id"), nullable=False)
    measure_id = Column(Integer, ForeignKey("climate_measure.id"), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)


    location = relationship("Location", back_populates="climate_historical_daily")
    measure = relationship("ClimateMeasure", back_populates="climate_historical_daily")
