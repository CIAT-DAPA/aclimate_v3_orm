from sqlalchemy import Column, BigInteger, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database.base import Base

class PhenologicalStageStress(Base):
    __tablename__ = 'phenological_stage_stress'

    id = Column(BigInteger, primary_key=True)
    stress_id = Column(Integer, ForeignKey('mng_stress.id'), nullable=False)
    phenological_stage_id = Column(Integer, ForeignKey('mng_phenological_stage.id'), nullable=False)
    max = Column(Float, nullable=False)
    min = Column(Float, nullable=False)
    enable = Column(Boolean, default=True)


    stress = relationship("MngStress", back_populates="phenological_stage_stresses")
    phenological_stage = relationship("MngPhenologicalStage", back_populates="phenological_stage_stresses")