from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class PhenologicalStageBase(BaseModel):
    crop_id: int = Field(..., gt=0, description="ID del cultivo")
    name: str = Field(..., max_length=255, description="Nombre de la etapa")
    short_name: Optional[str] = Field(None, max_length=50, description="Nombre corto")
    description: Optional[str] = Field(None, description="Descripción")
    order_stage: int = Field(..., description="Orden de la etapa")
    duration_avg_day: Optional[int] = Field(None, description="Duración promedio (días)")
    start_model: Optional[str] = Field(None, max_length=100, description="Modelo de inicio")
    end_model: Optional[str] = Field(None, max_length=100, description="Modelo de fin")

class PhenologicalStageCreate(PhenologicalStageBase):
    pass

class PhenologicalStageUpdate(BaseModel):
    crop_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    short_name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    order_stage: Optional[int] = None
    duration_avg_day: Optional[int] = None
    start_model: Optional[str] = Field(None, max_length=100)
    end_model: Optional[str] = Field(None, max_length=100)

class PhenologicalStageRead(PhenologicalStageBase):
    id: int
    model_config = ConfigDict(from_attributes=True)