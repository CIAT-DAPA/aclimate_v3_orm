from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime, timezone

class Admin1(Base):
    __tablename__ = 'admin_1'

    id = Column(BigInteger, primary_key=True)
    country_id = Column(Integer, ForeignKey('admin_country.id'), nullable=False)
    name = Column(String(255), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    country = relationship('Country', back_populates='admin_1')
    admin_2 = relationship('Admin2', back_populates='admin_1')
