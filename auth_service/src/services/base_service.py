import json
from abc import ABC, abstractmethod
from typing import Union

import backoff
from redis.exceptions import ConnectionError as conn_err_redis

from db.postgres_db import postgres
from db.redis_db import RedisCache
from models.models import User, Authentication, Role, User_Role, Permission
# from .utils.response_params import prepare_fields_for_response

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class AbstractBaseService(ABC):
    pass


class BaseService(AbstractBaseService):
    pass
