from pydantic import BaseModel
from models.value_objects import PermisionID
class Permission (BaseModel):
    """Модель разрешений."""

    id: PermisionID
    name: str
