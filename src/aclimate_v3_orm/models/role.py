from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from ..database.base import Base
from ..enums import Apps

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    app = Column(Enum(Apps), nullable=False)

    users = relationship('User', back_populates='role')
    accesses = relationship('UserAccess', back_populates='role', cascade='all, delete')
