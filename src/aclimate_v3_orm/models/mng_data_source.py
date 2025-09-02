from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngDataSource(Base):
    __tablename__ = 'mng_data_source'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('mng_country.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    content = Column(Text)

    # Relationships
    country = relationship("MngCountry", back_populates="data_sources")