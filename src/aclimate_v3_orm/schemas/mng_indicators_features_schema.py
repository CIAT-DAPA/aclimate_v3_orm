from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from ..enums import IndicatorFeatureType


class IndicatorFeatureBase(BaseModel):
    """Base fields for indicator features"""
    country_indicator_id: int = Field(..., gt=0, description="Country Indicator ID")
    title: str = Field(..., max_length=150, description="Feature title")
    description: Optional[str] = Field(None, description="Feature description")
    type: IndicatorFeatureType = Field(..., description="Type of indicator feature (recommendation or feature)")

    model_config = ConfigDict(use_enum_values=True)


class IndicatorFeatureCreate(BaseModel):
    """Schema for creating new indicator features (input validation only)"""
    country_indicator_id: int = Field(..., gt=0, description="Country Indicator ID")
    title: str = Field(..., max_length=150, description="Feature title")
    description: Optional[str] = Field(None, description="Feature description")
    type: IndicatorFeatureType = Field(..., description="Type of indicator feature (recommendation or feature)")

    model_config = ConfigDict(use_enum_values=True)


class IndicatorFeatureUpdate(BaseModel):
    """Schema for updating indicator features (all fields optional)"""
    title: Optional[str] = Field(None, max_length=150, description="Feature title")
    description: Optional[str] = Field(None, description="Feature description")
    type: Optional[IndicatorFeatureType] = Field(None, description="Type of indicator feature (recommendation or feature)")

    model_config = ConfigDict(use_enum_values=True)


class IndicatorFeatureRead(IndicatorFeatureBase):
    """Full indicator feature schema with read-only fields (ORM compatible)"""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
