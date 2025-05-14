from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class ClimateHistoricalClimatologyBase(BaseModel):
    """Base fields for climate climatology data"""
    location_id: int = Field(..., gt=0, description="ID of the location")
    measure_id: int = Field(..., gt=0, description="ID of the climate measure")
    month: int = Field(..., ge=1, le=12, description="Month number (1-12)")
    value: float = Field(..., description="Climatological value")

    @field_validator('month')
    @classmethod
    def validate_month(cls, v: int) -> int:
        """Ensure month is between 1 and 12"""
        if not 1 <= v <= 12:
            raise ValueError("Month must be between 1 and 12")
        return v

class ClimateHistoricalClimatologyCreate(ClimateHistoricalClimatologyBase):
    """Schema for creating new climatology records"""
    pass

class ClimateHistoricalClimatologyUpdate(BaseModel):
    """Schema for updating climatology records"""
    location_id: Optional[int] = Field(None, gt=0)
    measure_id: Optional[int] = Field(None, gt=0)
    month: Optional[int] = Field(None, ge=1, le=12)
    value: Optional[float] = None

    @field_validator('month')
    @classmethod
    def validate_month_update(cls, v: Optional[int]) -> Optional[int]:
        """Validate month if provided"""
        if v is not None and not 1 <= v <= 12:
            raise ValueError("Month must be between 1 and 12")
        return v

class ClimateHistoricalClimatologyRead(ClimateHistoricalClimatologyBase):
    """Complete climatology record including read-only fields"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)  # Enable ORM compatibility