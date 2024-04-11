from pydantic import BaseModel, Field
from datetime import datetime
from models.value_objects import UserID, AuthID, RoleID, PermisionID


class RolesSchema(BaseModel):
    uuid: RoleID = Field(..., validation_alias="id")
    type: str
    permissions: str


class PermissionsSchema(BaseModel):
    uuid: PermisionID = Field(..., validation_alias="id")
    name: str
