from sqlalchemy import Column, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database.base import Base
from ..enums.module import Modules

class UserAccess(Base):
    __tablename__ = 'user_access'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    country_id = Column(Integer, ForeignKey('mng_country.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    module = Column(Enum(Modules), primary_key=True, nullable=False)
    create = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    update = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)

    user = relationship('User', back_populates='accesses')
    role = relationship('Role', back_populates='accesses')
    country = relationship('MngCountry', back_populates='user_accesses')
