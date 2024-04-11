from pydantic import BaseModel, Field
from datetime import datetime

from models.value_objects import UserID, AuthID, RoleID, PermisionID


class UserSchema(BaseModel):
    uuid: UserID = Field(..., validation_alias="id")
    login: str
    firstname: str
    lastname: str
    created_at: datetime


class AuthenticationSchema(BaseModel):
    uuid: AuthID = Field(..., validation_alias="auth_id")
    user_id: UserID = Field(..., validation_alias="id")
    user_agent: str
    date_auth: datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
