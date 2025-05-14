from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngAdmin1(Base):
    __tablename__ = 'mng_admin_1'

    id = Column(BigInteger, primary_key=True)
    country_id = Column(Integer, ForeignKey('mng_country.id'), nullable=False)
    name = Column(String(255), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    country = relationship('MngCountry', back_populates='admin_1_regions')
    admin_2_regions = relationship('MngAdmin2', back_populates='admin_1_region')
