# forecast_analogue.py
from sqlalchemy import Column, BigInteger, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class ForecastAnalogue(Base):
    __tablename__ = 'forecast_analogue'

    id = Column(BigInteger, primary_key=True)
    forecast_id = Column(BigInteger, ForeignKey('forecast.id'), nullable=False)
    forecast = relationship("Forecast", back_populates="analogues")
    location_id = Column(BigInteger, ForeignKey('mng_location.id'), nullable=False)
    forecast_source = Column(String(100), nullable=False)
    indices_used = Column(String(255))
    year = Column(Integer, nullable=False)
    similarity_score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)