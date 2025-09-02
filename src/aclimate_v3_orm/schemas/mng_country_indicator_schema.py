from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

class CountryIndicatorBase(BaseModel):
    country_id: int = Field(..., description="Country ID")
    indicator_id: int = Field(..., description="Indicator ID")
    spatial_forecast: bool = Field(default=False, description="Whether the indicator should run spatially for forecast")
    spatial_climate: bool = Field(default=False, description="Whether the indicator should run spatially for climate")
    location_forecast: bool = Field(default=False, description="Whether the indicator should run by location for forecast")
    location_climate: bool = Field(default=False, description="Whether the indicator should run by location for climate")
    criteria: Optional[Dict] = Field(None, description="Configuration to determine at which level the indicator should run (e.g., full map, admin 1, admin 2)")

class CountryIndicatorCreate(BaseModel):
    country_id: int = Field(..., description="Country ID")
    indicator_id: int = Field(..., description="Indicator ID")
    spatial_forecast: bool = Field(default=False, description="Whether the indicator should run spatially for forecast")
    spatial_climate: bool = Field(default=False, description="Whether the indicator should run spatially for climate")
    location_forecast: bool = Field(default=False, description="Whether the indicator should run by location for forecast")
    location_climate: bool = Field(default=False, description="Whether the indicator should run by location for climate")
    criteria: Optional[Dict] = Field(None, description="Configuration to determine at which level the indicator should run (e.g., full map, admin 1, admin 2)")

class CountryIndicatorUpdate(BaseModel):
    spatial_forecast: Optional[bool] = None
    spatial_climate: Optional[bool] = None
    location_forecast: Optional[bool] = None
    location_climate: Optional[bool] = None
    criteria: Optional[Dict] = None

class CountryIndicatorRead(CountryIndicatorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
