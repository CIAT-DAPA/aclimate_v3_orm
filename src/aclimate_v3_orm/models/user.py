from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    keycloak_ext_id = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    role = relationship('Role', back_populates='users')
    accesses = relationship('UserAccess', back_populates='user')
