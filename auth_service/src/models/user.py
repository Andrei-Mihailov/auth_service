from pydantic import BaseModel
from datetime import datetime
from typing import Union

from models.value_objects import UserID


class User(BaseModel):
    """Модель пользователя на сайте."""

    id: UserID
    login: str
    first_name: Union[str, None]
    last_name: Union[str, None]
    password: bytes
    created_at: datetime = datetime.now
    active: bool = True
    is_admin: bool = False
    is_superuser: bool = False

    class Config:
        orm_mode = True
