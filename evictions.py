from collections import deque

class IndexedObject(object):
    """ value Object with index field, to be used with eviction classes for index lookup"""

    def __init__(self, val = None, *pointer):
        """
        val: actual value of the cache object/dict
        index = pointer to the indexed field/queue object for that particular key
        """
        self.val = val
        self.index = pointer


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


class LRU(BaseBehaviour):

    def __init__(self, limit_recs):
        super().__init__(limit_recs)
        self.queue = deque([], limit_recs)

    def update(self, key, value):
        """ writes to cache and updates the LRU queue"""
        if len(self.queue) == self.limit_records:
            self.queue.popleft()

        self.queue.remove(key)
        self.queue.append(key)
        self.cache.update({key: IndexedObject(value, key)})
        return value

    def get(self, key):
        """ updates the LRU queue for values that hit. else LRU is not updated"""

        value = self.cache.get(key)
        if value:
            if len(self.queue) == self.limit_records:
                self.queue.popleft()
            self.queue.append(key)
        return value
