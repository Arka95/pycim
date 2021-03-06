from evictions import *
from lib import *

class FallBack(metaclass=Singleton):

    def get(self, key, default=None):
        return default

    def update(self, key, value):
        return value


class Cim(metaclass=Singleton):

    def __init__(self, capacity=5000 , cache_type=None, fallback=None, default_val=None):
        """
        limit_records: maximum number of records to be allowed in the cache
        cache_type : currently only LRU is supported, will add MRU, LFU
        fallback: a get and update fallback for example a MongoFallback
        default_val: when key is absent, this will be returned from the fallback
        """

        self.default_val = default_val
        self.__write_policy = Policy.WRITE_THROUGH
        self.cache_type = cache_type or LRU(capacity)
        self.fallback = fallback

    def items(self):
        return self.cache_type.items()

    def update_capacity(self, capacity):
        self.cache_type.update_limits(capacity)

    def capacity(self):
        return self.cache_type.limit_records

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
        self.cache_type.clear()


    def set_fallback(self, fallback):
        self.fallback = fallback