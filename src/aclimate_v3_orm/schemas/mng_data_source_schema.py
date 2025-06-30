from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class DataSourceBase(BaseModel):
    country_id: int = Field(..., gt=0, description="ID del país")
    name: str = Field(..., max_length=255, description="Nombre de la fuente")
    description: Optional[str] = Field(None, description="Descripción")
    type: str = Field(..., max_length=50, description="Tipo de fuente")
    active: bool = Field(default=True, description="Activo")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    content: Optional[str] = Field(None, description="Contenido")

class DataSourceCreate(BaseModel):
    country_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    type: str = Field(..., max_length=50)
    active: bool = Field(default=True)
    content: Optional[str] = None

class DataSourceUpdate(BaseModel):
    country_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    type: Optional[str] = Field(None, max_length=50)
    active: Optional[bool] = None
    content: Optional[str] = None

class DataSourceRead(DataSourceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)