""" from pydantic import BaseModel, Field

from core.config import settings
from models.user import User


class UserParams(BaseModel):
    login: str = Field(description='Логин')
    firstname: str = Field(description='Имя', default=None)
    lastname: str = Field(description='Фамилия', default=None)
    password: str = Field(description='Пароль')


class UserEditParams(BaseModel):
    login: str = Field(description='Логин', default=None)
    firstname: str = Field(description='Имя', default=None)
    lastname: str = Field(description='Фамилия', default=None)
    password: str = Field(description='Пароль', default=None)


class AuthenticationParams(BaseModel):
    login: str = Field(description='Логин')
    password: str = Field(description='Пароль')


class TokenParams(BaseModel):
    access_token: str
    refresh_token: str


class RoleParams(BaseModel):
    type: str
    permissions: int


class RoleEditParams(BaseModel):
    type: str = Field(description='тип', default=None)
    permissions: int = Field(description='разрешения', default=None)


class PermissionsParams(BaseModel):
    name: str
 """