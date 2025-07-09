from sqlalchemy import Column, Integer, String, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from ..database.base import Base
from ..enums import StressCategory  # Debes definir este Enum en tu proyecto

class MngStress(Base):
    __tablename__ = 'mng_stress'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(100), nullable=False)
    category = Column(Enum(StressCategory), nullable=False)
    description = Column(Text)
    enable = Column(Boolean, default=True)

    phenological_stage_stresses = relationship("PhenologicalStageStress", back_populates="stress")