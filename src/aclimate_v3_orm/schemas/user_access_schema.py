from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from ..enums import Modules

class UserAccessBase(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    country_id: int = Field(..., gt=0, description="Country ID")
    role_id: int = Field(..., gt=0, description="Role ID")
    module: Modules = Field(..., description="Module name")
    create: bool = Field(default=False, description="Create permission")
    read: bool = Field(default=False, description="Read permission")
    update: bool = Field(default=False, description="Update permission")
    delete: bool = Field(default=False, description="Delete permission")

class UserAccessCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    country_id: int = Field(..., gt=0, description="Country ID")
    role_id: int = Field(..., gt=0, description="Role ID")
    module: Modules = Field(..., description="Module name")
    create: bool = Field(default=False, description="Create permission")
    read: bool = Field(default=False, description="Read permission")
    update: bool = Field(default=False, description="Update permission")
    delete: bool = Field(default=False, description="Delete permission")

class UserAccessUpdate(BaseModel):
    country_id: Optional[int] = Field(None, gt=0)
    role_id: Optional[int] = Field(None, gt=0)
    module: Optional[Modules] = None
    create: Optional[bool] = None
    read: Optional[bool] = None
    update: Optional[bool] = None
    delete: Optional[bool] = None

class UserAccessRead(UserAccessBase):
    country: Optional['CountryRead'] = None
    role: Optional['RoleRead'] = None
    model_config = ConfigDict(from_attributes=True)

# Import for forward references
from .mng_country_schema import CountryRead
from .role_schema import RoleRead
UserAccessRead.model_rebuild()
