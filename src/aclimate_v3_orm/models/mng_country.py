from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngCountry(Base):
    __tablename__ = 'mng_country'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    iso2 = Column(String(2), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    admin_1 = relationship('MngAdmin1', back_populates='country')
