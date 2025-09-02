from datetime import date as Date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .mng_location_schema import LocationRead
from .mng_climate_measure_schema import ClimateMeasureRead

class ClimateHistoricalMonthlyBase(BaseModel):
    """Base fields for monthly climate historical data"""
    location_id: int = Field(..., gt=0, description="ID of the location")
    measure_id: int = Field(..., gt=0, description="ID of the climate measure")
    date: Date = Field(..., description="Date of the measurement (first day of month)")
    value: float = Field(..., description="Measured value")

class ClimateHistoricalMonthlyCreate(ClimateHistoricalMonthlyBase):
    """Schema for creating new monthly climate records"""
    pass

class ClimateHistoricalMonthlyUpdate(BaseModel):
    """Schema for updating monthly climate records"""
    location_id: Optional[int] = Field(None, gt=0)
    measure_id: Optional[int] = Field(None, gt=0)
    date: Optional[Date] = None
    value: Optional[float] = None

class ClimateHistoricalMonthlyRead(ClimateHistoricalMonthlyBase):
    """Complete monthly climate record including read-only fields"""
    id: int
    
    location: Optional[LocationRead] = None
    measure: Optional[ClimateMeasureRead] = None
    
    model_config = ConfigDict(from_attributes=True)