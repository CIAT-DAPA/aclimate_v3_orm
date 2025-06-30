from sqlalchemy import Column, BigInteger, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class Forecast(Base):
    __tablename__ = 'forecast'

    id = Column(BigInteger, primary_key=True)
    run_date = Column(Date, nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    analogues = relationship("ForecastAnalogue", back_populates="forecast")