from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngAdmin2(Base):
    __tablename__ = 'mng_admin_2'

    id = Column(BigInteger, primary_key=True)
    admin_1_id = Column(BigInteger, ForeignKey('mng_admin_1.id'), nullable=False)
    name = Column(String(255), nullable=False)
    ext_id = Column(String(255), default='')
    visible = Column(Boolean, default=True)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    admin_1 = relationship('MngAdmin1', back_populates='admin_2')
    
    location = relationship('MngLocation', back_populates='admin_2')