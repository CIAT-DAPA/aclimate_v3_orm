from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database.base import Base
from ..enums import Apps

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    app = Column(Enum(Apps), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    users = relationship('User', back_populates='role')
    accesses = relationship('UserAccess', back_populates='role', cascade='all, delete')
