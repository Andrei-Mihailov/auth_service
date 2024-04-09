from pydantic import BaseModel
from datetime import datetime
from models.value_objects import AuthID, UserID
class Authentication(BaseModel):
      """Модель аутификации."""

      id: AuthID
      user_id: UserID;
      user_agent: str;
      date_auth: datetime;
