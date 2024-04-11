from fastapi import Depends, HTTPException, status


from models.user import User
from db.postgres_db import postgres
from db.redis_db import RedisCache, get_redis
from models.user import User
from .base_service import BaseService


class PermissionsService(BaseService):
    pass
