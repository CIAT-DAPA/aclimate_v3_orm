from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class HistoricalAgroclimaticIndicatorBase(BaseModel):
    indicator_id: int = Field(..., gt=0)
    location_id: int = Field(..., gt=0)
    phenological_id: int = Field(..., gt=0)
    value: float = Field(..., description="Valor del indicador")
    start_date: date
    end_date: date

class HistoricalAgroclimaticIndicatorCreate(HistoricalAgroclimaticIndicatorBase):
    pass

class HistoricalAgroclimaticIndicatorUpdate(BaseModel):
    indicator_id: Optional[int] = Field(None, gt=0)
    location_id: Optional[int] = Field(None, gt=0)
    phenological_id: Optional[int] = Field(None, gt=0)
    value: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class HistoricalAgroclimaticIndicatorRead(HistoricalAgroclimaticIndicatorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)