# mng_configuration_file.py
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class MngConfigurationFile(Base):
    __tablename__ = 'mng_configuration_file'

    id = Column(BigInteger, primary_key=True)
    setup_id = Column(BigInteger, ForeignKey('mng_setup.id'), nullable=False)
    name = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    setup = relationship("MngSetup", back_populates="configuration_files")