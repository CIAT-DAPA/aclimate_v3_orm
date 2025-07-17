from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .mng_crop_schema import CropRead
from .mng_location_schema import LocationRead

class SeasonBase(BaseModel):
    location_id: int = Field(..., gt=0)
    crop_id: int = Field(..., gt=0)
    planting_start: date
    planting_end: date
    season_start: date
    season_end: date
    enable: Optional[bool] = Field(default=True, description="Habilitado")
class SeasonCreate(SeasonBase):
    pass

class SeasonUpdate(BaseModel):
    location_id: Optional[int] = Field(None, gt=0)
    crop_id: Optional[int] = Field(None, gt=0)
    planting_start: Optional[date] = None
    planting_end: Optional[date] = None
    season_start: Optional[date] = None
    season_end: Optional[date] = None
    enable: Optional[bool] = Field(default=True)

class SeasonRead(SeasonBase):
    id: int
    location: Optional[LocationRead] = None
    crop: Optional[CropRead] = None
    model_config = ConfigDict(from_attributes=True)