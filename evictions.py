from deque import Deque

class IndexedObject(object):
    """ value Object with index field, to be used with eviction classes for index lookup"""

    def __init__(self, val, pointer):
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

    def clear(self):
        self.cache.clear()

class LRU(BaseBehaviour):

    def __init__(self, limit_recs):
        super().__init__(limit_recs)
        self.queue = Deque(capacity=limit_recs)

    def remove(self, key):
        node = self.cache.get(key)
        if not node:
            return
        self.queue.remove(node.index)
        del self.cache[key]

    def update(self, key, value):
        """ writes to cache and updates the LRU queue"""
        if self.queue.size() == self.limit_records and self.cache.get(key) is None:
            self.queue.pop_left()

        self.remove(key)
        index = self.queue.append(key)
        self.cache.update({key: IndexedObject(value, index)})
        return value

    def get(self, key):
        """ updates the LRU queue for values that hit. else LRU is not updated"""

        node = self.cache.get(key)
        if node:
            self.queue.move_to_back(node.index)
            return node.val
        return None
