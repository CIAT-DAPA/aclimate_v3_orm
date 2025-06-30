# mng_data_source.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from ..database.base import Base
from datetime import datetime, timezone

class MngDataSource(Base):
    __tablename__ = 'mng_data_source'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    content = Column(Text)