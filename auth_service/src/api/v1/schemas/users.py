from pydantic import BaseModel, Field
from datetime import datetime

from models.value_objects import UserID


class UserSchema(BaseModel):
    uuid: UserID = Field(..., validation_alias="id")
    login: str
    firstname: str
    lastname: str
    #created_at: datetime


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
