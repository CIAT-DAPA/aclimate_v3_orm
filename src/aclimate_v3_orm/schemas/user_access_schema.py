from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserAccessBase(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    country_id: int = Field(..., gt=0, description="Country ID")
    role_id: int = Field(..., gt=0, description="Role ID")
    create: bool = Field(default=False, description="Create permission")
    read: bool = Field(default=False, description="Read permission")
    update: bool = Field(default=False, description="Update permission")
    delete: bool = Field(default=False, description="Delete permission")

class UserAccessCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    country_id: int = Field(..., gt=0, description="Country ID")
    role_id: int = Field(..., gt=0, description="Role ID")
    create: bool = Field(default=False, description="Create permission")
    read: bool = Field(default=False, description="Read permission")
    update: bool = Field(default=False, description="Update permission")
    delete: bool = Field(default=False, description="Delete permission")

class UserAccessUpdate(BaseModel):
    country_id: Optional[int] = Field(None, gt=0)
    role_id: Optional[int] = Field(None, gt=0)
    create: Optional[bool] = None
    read: Optional[bool] = None
    update: Optional[bool] = None
    delete: Optional[bool] = None

class UserAccessRead(UserAccessBase):
    model_config = ConfigDict(from_attributes=True)
