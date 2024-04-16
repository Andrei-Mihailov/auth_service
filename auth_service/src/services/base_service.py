from abc import ABC

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class AbstractBaseService(ABC):
    pass


class BaseService(AbstractBaseService):
    pass
