from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .mng_stress_schema import StressRead
from .mng_phenological_stage_schema import PhenologicalStageRead

class PhenologicalStageStressBase(BaseModel):
    stress_id: int = Field(..., gt=0)
    phenological_stage_id: int = Field(..., gt=0)
    max: float = Field(..., description="Valor máximo")
    min: float = Field(..., description="Valor mínimo")
    enable: bool = Field(default=True, description="Habilitado")

class PhenologicalStageStressCreate(PhenologicalStageStressBase):
    pass

class PhenologicalStageStressUpdate(BaseModel):
    stress_id: Optional[int] = Field(None, gt=0)
    phenological_stage_id: Optional[int] = Field(None, gt=0)
    max: Optional[float] = None
    min: Optional[float] = None
    enable: Optional[bool] = Field(True, description="Indica si la relación está habilitada")

class PhenologicalStageStressRead(PhenologicalStageStressBase):
    id: int
    stress: Optional[StressRead] = None
    phenological_stage: Optional[PhenologicalStageRead] = None
    model_config = ConfigDict(from_attributes=True)