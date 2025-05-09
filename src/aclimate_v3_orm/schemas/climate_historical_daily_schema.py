from datetime import date as Date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ClimateHistoricalDailyBase(BaseModel):
    """Base fields for daily climate historical data"""
    location_id: int = Field(..., gt=0, description="ID of the location")
    measure_id: int = Field(..., gt=0, description="ID of the climate measure")
    date: Date = Field(..., description="Date of the measurement")
    value: float = Field(..., description="Daily measured value")

class ClimateHistoricalDailyCreate(ClimateHistoricalDailyBase):
    """Schema for creating new daily climate records"""
    pass

class ClimateHistoricalDailyUpdate(BaseModel):
    """Schema for updating daily climate records"""
    location_id: Optional[int] = Field(None, gt=0)
    measure_id: Optional[int] = Field(None, gt=0)
    date: Optional[Date] = None
    value: Optional[float] = None

class ClimateHistoricalDailyRead(ClimateHistoricalDailyBase):
    """Complete daily climate record including read-only fields"""
    id: int
    
    # Relationships (uncomment if needed in responses)
    # location: Optional['Location'] = None
    # measure: Optional['ClimateMeasure'] = None
    
    model_config = ConfigDict(from_attributes=True)  # Enable ORM compatibility