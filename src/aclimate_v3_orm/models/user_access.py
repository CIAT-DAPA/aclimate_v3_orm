from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class UserAccess(Base):
    __tablename__ = 'user_access'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    country_id = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    create = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    update = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)

    user = relationship('User', back_populates='accesses')
    role = relationship('Role', back_populates='accesses')
