from sqlalchemy import Column, BigInteger, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from aclimate_v3_orm.database.base import Base

class ClimateHistoricalDaily(Base):
    __tablename__ = 'climate_historical_daily'

    id = Column(BigInteger, primary_key=True)
    location_id = Column(BigInteger, ForeignKey("mng_location.id"), nullable=False)
    measure_id = Column(Integer, ForeignKey("mng_climate_measure.id"), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)

    location = relationship("MngLocation", back_populates="daily_measurements")
    measure = relationship("MngClimateMeasure", back_populates="daily_measurements")