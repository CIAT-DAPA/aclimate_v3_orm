from sqlalchemy import Column, BigInteger, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database.base import Base

class MngSeason(Base):
    __tablename__ = 'mng_season'

    id = Column(BigInteger, primary_key=True)
    location_id = Column(BigInteger, ForeignKey('mng_location.id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('mng_crop.id'), nullable=False)
    planting_start = Column(Date, nullable=False)
    planting_end = Column(Date, nullable=False)
    season_start = Column(Date, nullable=False)
    season_end = Column(Date, nullable=False)
    enable = Column(Boolean, default=True)

    # Relaciones
    location = relationship("MngLocation", back_populates="seasons")
    crop = relationship("MngCrop", back_populates="seasons")

    setups = relationship("MngSetup", back_populates="season")