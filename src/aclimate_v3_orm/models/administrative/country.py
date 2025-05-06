from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime, timezone

class Country(Base):
    __tablename__ = 'admin_country'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    iso2 = Column(String(50), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    admin_1 = relationship('Admin1', back_populates='country')
