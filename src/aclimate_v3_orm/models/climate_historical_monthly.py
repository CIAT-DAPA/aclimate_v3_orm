from sqlalchemy import Column, BigInteger, Integer, Date, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..database.base import Base

class ClimateHistoricalMonthly(Base):
    __tablename__ = 'climate_historical_monthly'

    id = Column(BigInteger, primary_key=True)
    location_id = Column(BigInteger, ForeignKey("mng_location.id"), nullable=False)
    measure_id = Column(Integer, ForeignKey("mng_climate_measure.id"), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)

    __table_args__ = (
        Index('ix_monthly_location', location_id),
        Index('ix_monthly_location_date', location_id, date),
        Index('ix_monthly_location_measure', location_id, measure_id),
        Index('ix_monthly_location_measure_date', location_id, measure_id, date, unique=True),
        Index('ix_monthly_date', date),
    )

    location = relationship("MngLocation", back_populates="monthly_measurements")
    measure = relationship("MngClimateMeasure", back_populates="monthly_measurements")