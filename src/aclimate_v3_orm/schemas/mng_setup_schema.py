# mng_setup_schema.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class SetupBase(BaseModel):
    cultivar_id: int = Field(..., description="Cultivar ID reference")
    soil_id: int = Field(..., description="Soil ID reference")
    season_id: int = Field(..., description="Season ID reference")
    frequency: int = Field(..., description="Frequency value")
    enable: bool = Field(default=True, description="Enable status")
    registered_at: Optional[datetime] = Field(None, alias="register")
    updated_at: Optional[datetime] = Field(None, alias="updated")

class SetupCreate(BaseModel):
    cultivar_id: int
    soil_id: int
    season_id: int
    frequency: int
    enable: bool = True

class SetupUpdate(BaseModel):
    cultivar_id: Optional[int] = None
    soil_id: Optional[int] = None
    season_id: Optional[int] = None
    frequency: Optional[int] = None
    enable: Optional[bool] = None

class SetupRead(SetupBase):
    id: int
    model_config = ConfigDict(from_attributes=True)