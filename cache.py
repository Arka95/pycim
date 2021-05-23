class Singleton(type):
    # TODO: move this to a separate file
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

from collections import deque


class Policy:
    # TODO: write_back implementation
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"


class BaseBehaviour(object):
    """Defines default behaviour if no updation policies are used"""

    def __init__(self, limit_recs):
        self.cache = {}
        self.limit_records = limit_recs

    def get(self, key):
        return self.cache.get(key)

    def update(self, key, value):
        if len(self.cache) != self.limit_records:
            self.cache.update({key: value})
            return value
        return None


class FallBack(metaclass=Singleton):

    def get(self, key, default=None):
        return default

    def update(self, key, value):
        return value


class LRU(BaseBehaviour):

    def __init__(self, limit_recs):
        super().__init__(limit_recs)
        self.queue = deque([], limit_recs)


    def update(self, key, value):
        """ writes to cache and updates the LRU queue"""
        if len(self.queue) == self.limit_records:
            self.queue.popleft()

        self.queue.append(key)
        self.cache.update({key:value})
        return value


    def get(self, key):
        """ updates the LRU queue for values that hit. else LRU is not updated"""

        value = self.cache.get(key)
        if value:
            if len(self.queue) == self.limit_records:
                self.queue.popleft()
            self.queue.append(key)
        return value


class Cim(metaclass=Singleton):

    def __init__(self, limit_records=5000 , cache_type=None, fallback=None, default_val=None):
        """
        limit_records: maximum number of records to be allowed in the cache
        cache_type : currentl only LRU is supported, will add MRU, LFU
        fallback: a get and update fallback for example a MongoFallback
        default_val: when key is absent, this will be returned from the fallback
        """

        self.default_val = default_val
        self.__write_policy = Policy.WRITE_THROUGH
        self.cache_type = cache_type or LRU(limit_records)
        self.fallback = fallback


    def get(self, key):
        """ retuieves values from cache. If not present, tries fetching from fallback
        and updates cache with fallback result"""

        res = self.cache_type.get(key)

        if res :
            return res

        if not self.fallback:
            return self.default_val

        value =  self.fallback.get(key)
        if value:
            self.cache_type.update(key, value)
        return value


    def update(self, key, value):
        res =  self.cache_type.update(key, value)

        if self.__write_policy== Policy.WRITE_THROUGH and self.fallback!=None:
            return self.fallback.update(key, value)
        return res


    def set_cache_type(self, cache_type):
        self.cache_type = cache_type


    def set_write_policy(self, wp):
        self.__write_policy = wp


    def size(self):
        return len(self.cache_type.cache)


    def clear(self):
        self.cache_type.cache.clear()


    def set_fallback(self, fallback):
        self.fallback = fallback