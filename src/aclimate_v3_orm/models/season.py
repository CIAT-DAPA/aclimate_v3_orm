from sqlalchemy import Column, BigInteger, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class Season(Base):
    __tablename__ = 'season'

    id = Column(BigInteger, primary_key=True)
    location_id = Column(BigInteger, ForeignKey('mng_location.id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('mng_crop.id'), nullable=False)
    planting_start = Column(Date, nullable=False)
    planting_end = Column(Date, nullable=False)
    season_start = Column(Date, nullable=False)
    season_end = Column(Date, nullable=False)

    # Relaciones
    location = relationship("MngLocation", back_populates="seasons")
    crop = relationship("MngCrop", back_populates="seasons")

    setups = relationship("MngSetup", back_populates="season")