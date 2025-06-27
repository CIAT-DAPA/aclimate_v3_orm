from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from ..enums import Period
from .mng_indicators_schema import IndicatorRead

# ========== ClimateHistoricalIndicator Schemas ==========
class ClimateHistoricalIndicatorBase(BaseModel):
    """Base fields for historical indicator data"""
    indicator_id: int = Field(..., gt=0, description="ID of the related indicator")
    location_id: int = Field(..., gt=0, description="ID of the related location")
    value: float = Field(..., description="Numeric value of the indicator")
    period: Period = Field(..., description="Time period classification")
    start_date: date = Field(..., description="Start date of the measurement period")
    end_date: Optional[date] = Field(None, description="Optional end date of the measurement period")

    model_config = ConfigDict(use_enum_values=True)

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_dates(cls, v: date, values) -> date:
        """Validate date consistency"""
        if 'end_date' in values.data and values.data['end_date'] is not None:
            if v > values.data['end_date']:
                raise ValueError("Start date cannot be after end date")
        return v

class ClimateHistoricalIndicatorCreate(BaseModel):
    """Schema for creating new historical records"""
    indicator_id: int = Field(..., gt=0, description="ID of the related indicator")
    location_id: int = Field(..., gt=0, description="ID of the related location")
    value: float = Field(..., description="Numeric value of the indicator")
    period: Period = Field(..., description="Time period classification")
    start_date: date = Field(..., description="Start date of the measurement period")
    end_date: Optional[date] = Field(None, description="Optional end date of the measurement period")

class ClimateHistoricalIndicatorUpdate(BaseModel):
    """Schema for updating historical records (all fields optional)"""
    indicator_id: Optional[int] = Field(None, gt=0)
    location_id: Optional[int] = Field(None, gt=0)
    value: Optional[float] = None
    period: Optional[Period] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_dates_update(cls, v: Optional[date], values) -> Optional[date]:
        """Validate date consistency during updates"""
        if v is not None and 'end_date' in values.data and values.data['end_date'] is not None:
            if v > values.data['end_date']:
                raise ValueError("Start date cannot be after end date")
        return v

class ClimateHistoricalIndicatorRead(ClimateHistoricalIndicatorBase):
    """Complete historical record including read-only fields (ORM compatible)"""
    id: int
    indicator: Optional[IndicatorRead] = None
    model_config = ConfigDict(from_attributes=True)