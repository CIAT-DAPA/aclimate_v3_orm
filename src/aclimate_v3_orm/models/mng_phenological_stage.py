# mng_phenological_stage.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database.base import Base

class MngPhenologicalStage(Base):
    __tablename__ = 'mng_phenological_stage'

    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey('mng_crop.id'), nullable=False)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50))
    description = Column(Text)
    order_stage = Column(Integer, nullable=False)
    duration_avg_day = Column(Integer)
    start_model = Column(String(100))
    end_model = Column(String(100))
    enable = Column(Boolean, default=True)

    # Relationship
    crop = relationship("MngCrop", back_populates="stages")

    historical_agroclimatic_indicators = relationship("HistoricalAgroclimaticIndicator", back_populates="phenological_stage")
    phenological_stage_stresses = relationship("PhenologicalStageStress", back_populates="phenological_stage")