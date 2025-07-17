from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ForecastBase(BaseModel):
    country_id: int = Field(..., gt=0, description="ID of the country")
    run_date: date = Field(..., description="The date when the forecast was run")
    enable: bool = Field(default=True, description="Whether the forecast is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class ForecastCreate(BaseModel):
    country_id: int
    run_date: date
    enable: bool = True

class ForecastUpdate(BaseModel):
    run_date: Optional[date] = None
    enable: Optional[bool] = None

class ForecastRead(ForecastBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )