from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from .mng_country_schema import CountryRead
from .mng_climate_measure_schema import ClimateMeasureRead


class CountryClimateMeasureBase(BaseModel):
    country_id: int = Field(..., gt=0, description="Country ID")
    measure_id: int = Field(..., gt=0, description="Climate measure ID")
    spatial_forecast: bool = Field(default=False, description="Whether the measure should run spatially for forecast")
    spatial_climate: bool = Field(default=False, description="Whether the measure should run spatially for climate")
    location_forecast: bool = Field(default=False, description="Whether the measure should run by location for forecast")
    location_climate: bool = Field(default=False, description="Whether the measure should run by location for climate")
    description: Optional[str] = Field(None, description="Country-specific description of the climate measure")
    store: Optional[str] = Field(None, max_length=255, description="Store path or identifier (optional, only if special)")
    workspace: Optional[str] = Field(None, max_length=255, description="Workspace identifier (optional, only if special)")


class CountryClimateMeasureCreate(BaseModel):
    country_id: int = Field(..., gt=0, description="Country ID")
    measure_id: int = Field(..., gt=0, description="Climate measure ID")
    spatial_forecast: bool = Field(default=False, description="Whether the measure should run spatially for forecast")
    spatial_climate: bool = Field(default=False, description="Whether the measure should run spatially for climate")
    location_forecast: bool = Field(default=False, description="Whether the measure should run by location for forecast")
    location_climate: bool = Field(default=False, description="Whether the measure should run by location for climate")
    description: Optional[str] = Field(None, description="Country-specific description of the climate measure")
    store: Optional[str] = Field(None, max_length=255, description="Store path or identifier (optional, only if special)")
    workspace: Optional[str] = Field(None, max_length=255, description="Workspace identifier (optional, only if special)")


class CountryClimateMeasureUpdate(BaseModel):
    spatial_forecast: Optional[bool] = None
    spatial_climate: Optional[bool] = None
    location_forecast: Optional[bool] = None
    location_climate: Optional[bool] = None
    description: Optional[str] = None
    store: Optional[str] = None
    workspace: Optional[str] = None


class CountryClimateMeasureRead(CountryClimateMeasureBase):
    id: int
    country: Optional[CountryRead] = None
    measure: Optional[ClimateMeasureRead] = None

    model_config = ConfigDict(from_attributes=True)