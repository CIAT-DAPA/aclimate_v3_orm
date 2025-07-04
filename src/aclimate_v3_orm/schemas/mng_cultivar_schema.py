from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CultivarBase(BaseModel):
    country_id: int = Field(..., gt=0, description="ID del país")
    crop_id: int = Field(..., gt=0, description="ID del cultivo")
    name: str = Field(..., max_length=255, description="Nombre del cultivar")
    sort_order: int = Field(..., description="Orden")
    rainfed: bool = Field(default=False, description="Secano")
    enable: bool = Field(default=True, description="Habilitado")
    register: Optional[datetime] = Field(None, description="Fecha de registro")
    updated: Optional[datetime] = Field(None, description="Fecha de actualización")

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
    model_config = ConfigDict(from_attributes=True)