from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from ..enums import Period
from .mng_country_schema import CountryRead
from .mng_climate_measure_schema import ClimateMeasureRead


class SpatialClimateConf(BaseModel):
    temporality: Period
    store: Optional[str] = Field(None, max_length=255, description="Store path or identifier")
    workspace: Optional[str] = Field(None, max_length=255, description="Workspace identifier")

    model_config = ConfigDict(use_enum_values=True)


class CountryClimateMeasureBase(BaseModel):
    country_id: int = Field(..., gt=0, description="Country ID")
    measure_id: int = Field(..., gt=0, description="Climate measure ID")
    spatial_forecast: bool = Field(default=False, description="Whether the measure should run spatially for forecast")
    spatial_climate: bool = Field(default=False, description="Whether the measure should run spatially for climate")
    location_forecast: bool = Field(default=False, description="Whether the measure should run by location for forecast")
    location_climate: bool = Field(default=False, description="Whether the measure should run by location for climate")
    spatial_climate_conf: Optional[List[SpatialClimateConf]] = Field(None, description="Per-temporality store/workspace configuration for spatial climate")
    location_climate_conf: Optional[List[Period]] = Field(None, description="List of time periods supported by the country climate measure for location climate")
    description: Optional[str] = Field(None, description="Country-specific description of the climate measure")


class CountryClimateMeasureCreate(BaseModel):
    country_id: int = Field(..., gt=0, description="Country ID")
    measure_id: int = Field(..., gt=0, description="Climate measure ID")
    spatial_forecast: bool = Field(default=False, description="Whether the measure should run spatially for forecast")
    spatial_climate: bool = Field(default=False, description="Whether the measure should run spatially for climate")
    location_forecast: bool = Field(default=False, description="Whether the measure should run by location for forecast")
    location_climate: bool = Field(default=False, description="Whether the measure should run by location for climate")
    spatial_climate_conf: Optional[List[SpatialClimateConf]] = Field(None, description="Per-temporality store/workspace configuration for spatial climate")
    location_climate_conf: Optional[List[Period]] = Field(None, description="List of time periods supported by the country climate measure for location climate")
    description: Optional[str] = Field(None, description="Country-specific description of the climate measure")


class CountryClimateMeasureUpdate(BaseModel):
    spatial_forecast: Optional[bool] = None
    spatial_climate: Optional[bool] = None
    location_forecast: Optional[bool] = None
    location_climate: Optional[bool] = None
    spatial_climate_conf: Optional[List[SpatialClimateConf]] = None
    location_climate_conf: Optional[List[Period]] = None
    description: Optional[str] = None


class CountryClimateMeasureRead(CountryClimateMeasureBase):
    id: int
    country: Optional[CountryRead] = None
    measure: Optional[ClimateMeasureRead] = None

    model_config = ConfigDict(from_attributes=True)