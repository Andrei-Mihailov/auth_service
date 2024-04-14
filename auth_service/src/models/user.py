from pydantic import BaseModel
from datetime import datetime
from models.value_objects import UserID


class User(BaseModel):
    """Модель пользователя на сайте."""

    user_id: UserID
    first_name: str | None
    last_name: str | None
    user_name: str
    password: bytes
    created_at: datetime = datetime.now
    active: bool = True
