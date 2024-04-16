from pydantic import BaseModel, Field
from datetime import datetime

from models.value_objects import UserID, AuthID


class AuthenticationSchema(BaseModel):
    uuid: AuthID = Field(..., validation_alias="auth_id")
    user_id: UserID = Field(..., validation_alias="id")
    user_agent: str
    date_auth: datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class AuthenticationParams(BaseModel):
    login: str = Field(description="Логин")
    password: str = Field(description="Пароль")


class TokenParams(BaseModel):
    access_token: str
    refresh_token: str
