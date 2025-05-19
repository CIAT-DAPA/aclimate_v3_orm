from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone
from ..enums import SourceType

class MngSource(Base):
    __tablename__ = 'mng_source'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    source_type = Column(Enum(SourceType), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    location = relationship("MngLocation", back_populates="source")
