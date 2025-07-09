from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ForecastAnalogueBase(BaseModel):
    forecast_id: int = Field(..., gt=0, description="ID del forecast")
    location_id: int = Field(..., gt=0, description="ID de la ubicación")
    forecast_source: str = Field(..., max_length=100, description="Fuente del pronóstico")
    indices_used: Optional[str] = Field(None, max_length=255, description="Índices utilizados")
    year: int = Field(..., description="Año")
    similarity_score: float = Field(..., description="Score de similitud")
    rank: int = Field(..., description="Ranking")

class ForecastAnalogueCreate(ForecastAnalogueBase):
    pass

class ForecastAnalogueUpdate(BaseModel):
    forecast_id: Optional[int] = Field(None, gt=0)
    location_id: Optional[int] = Field(None, gt=0)
    forecast_source: Optional[str] = Field(None, max_length=100)
    indices_used: Optional[str] = Field(None, max_length=255)
    year: Optional[int] = None
    similarity_score: Optional[float] = None
    rank: Optional[int] = None

class ForecastAnalogueRead(ForecastAnalogueBase):
    id: int
    model_config = ConfigDict(from_attributes=True)