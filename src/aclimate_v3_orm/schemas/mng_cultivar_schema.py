from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .mng_country_schema import CountryRead
from .mng_crop_schema import CropRead

class CultivarBase(BaseModel):
    country_id: int = Field(..., gt=0, description="ID del país")
    crop_id: int = Field(..., gt=0, description="ID del cultivo")
    name: str = Field(..., max_length=255, description="Nombre del cultivar")
    sort_order: int = Field(..., description="Orden")
    rainfed: bool = Field(default=False, description="Secano")
    enable: bool = Field(default=True, description="Habilitado")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class CultivarCreate(BaseModel):
    country_id: int = Field(..., gt=0)
    crop_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=255)
    sort_order: int = Field(...,)
    rainfed: bool = Field(default=False)
    enable: bool = Field(default=True)

class CultivarUpdate(BaseModel):
    country_id: Optional[int] = Field(None, gt=0)
    crop_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    sort_order: Optional[int] = None
    rainfed: Optional[bool] = None
    enable: Optional[bool] = None

class CultivarRead(CultivarBase):
    id: int
    country: Optional[CountryRead] = None
    crop: Optional[CropRead] = None
    model_config = ConfigDict(from_attributes=True)