from pydantic import BaseModel, Field
from typing import Union

from models.value_objects import UserID


class UserSchema(BaseModel):
    uuid: UserID = Field(..., validation_alias="id")
    login: str
    first_name: Union[str, None]
    last_name: Union[str, None]
    # created_at: datetime


class UserParams(BaseModel):
    login: str = Field(description="Логин")
    first_name: Union[str, None] = Field(description="Имя", default=None, allow_none=True)
    last_name: Union[str, None] = Field(description="Фамилия", default=None, allow_none=True)
    password: str = Field(description="Пароль")


class UserEditParams(BaseModel):
    login: str = Field(description="Логин", default=None)
    first_name: str = Field(description="Имя", default=None)
    last_name: str = Field(description="Фамилия", default=None)
    password: str = Field(description="Пароль", default=None)
