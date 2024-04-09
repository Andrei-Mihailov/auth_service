from pydantic import BaseModel
from datetime import datetime
from models.value_objects import UserID
class User (BaseModel):
    """Модель пользователя на сайте."""

    user_id: UserID
    first_name: str
    last_name: str
    user_name: str
    password: str
    created_at: datetime