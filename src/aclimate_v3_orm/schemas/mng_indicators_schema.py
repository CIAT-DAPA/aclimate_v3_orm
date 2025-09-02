from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from ..enums import IndicatorsType
from .mng_indicator_category_schema import IndicatorCategoryRead

class IndicatorBase(BaseModel):
    """Base fields for indicators"""
    type: IndicatorsType = Field(..., description="Type of indicator")
    name: str = Field(..., max_length=150)
    short_name: str = Field(..., max_length=50)
    unit: str = Field(..., max_length=25)
    description: Optional[str] = None
    indicator_category_id: int = Field(..., gt=0, description="Category ID for the indicator")
    enable: Optional[bool] = Field(default=True, description="Whether the source is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

    model_config = ConfigDict(use_enum_values=True)

class IndicatorCreate(BaseModel):
    """Schema for creating new indicators (input validation only)"""
    type: IndicatorsType = Field(..., description="Type of indicator")
    name: str = Field(..., max_length=150)
    short_name: str = Field(..., max_length=50)
    unit: str = Field(..., max_length=25)
    description: Optional[str] = None
    indicator_category_id: int = Field(..., gt=0, description="Category ID for the indicator")
    enable: Optional[bool] = Field(default=True, description="Whether the source is enabled")

class IndicatorUpdate(BaseModel):
    """Schema for updating indicators (all fields optional)"""
    type: Optional[IndicatorsType] = None
    name: Optional[str] = Field(None, max_length=150)
    short_name: Optional[str] = Field(None, max_length=50)
    unit: Optional[str] = Field(None, max_length=25)
    description: Optional[str] = None
    indicator_category_id: Optional[int] = Field(None, gt=0, description="Category ID for the indicator")
    enable: Optional[bool] = Field(default=True, description="Whether the source is enabled")


class IndicatorRead(IndicatorBase):
    """Full indicator schema with read-only fields (ORM compatible)"""
    id: int
    category: Optional[IndicatorCategoryRead] = None
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )