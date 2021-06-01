Cim (Cache in Memory Singleton) is what you would like to interpret as an in-memory key, value store in python. its methods are similar to that of a map.

##Attributes:

you can specify each of these in the constructor as well. (check definition)
- **default_val** : default return value if key not present. (default is None)
- **capacity**: The capaity of the cache. Default is 5000 items(keys)
- **cache_type:** how the cache behaves with updates (default is LRU. Cache behaviors are implemented in evictions.py. please google Beahvioral patterns in OOPS for more information)
  Current options for cache type are MRU, LRU and CacheBehavior. BaseBehavior is the Base class which does not use any queued eviction policies and stops cache updation after limit is reached
- **fallback**: A fallback for the cache. Whenever there is a cache miss, the cache will try to lookup and update with this source.
  Fallback is a singleton abstract class with get and update methods. For exampleyou can have a fallback to mongodb inheriting ths Fallback class and implement get and update for that mongodb.
  By default, Fallback is None.
  
##Usage:

    c = Cim(capacity=5)
    c.update(1,'a')
    c.update(2,'a')
    c.update(3,'a')
    c.get(3)
    'c'

####If you want to view how the LRU/MRU queue is being managed:

    c.cache_type
    <evictions.LRU at 0x7fa48f7c0580>
    
    # shows you the queue items. here queue is a locally impemented linked-list based deque (from deque.py)
    c.cache_type.queue.to_list()
    [1, 2, 3]

####You can change the cache capaity using update_capacity(new_size). 

If your cache size is currently > your new capacity, the excess, most irrelevant items based on the vcache behaviur, will be removed. However if the new capacity is big enough, items will be preserved

    c.update_capacity(10)
    c.cache_type.queue.to_list()
    [1, 2, 3]
    c.update_capacity(2)
    c.cache_type.queue.to_list()
    [2, 3]

####You can change the cache behavior in running code as well.

    c.set_cache_type(MRU(5))
    c.cache_type
    <evictions.MRU at 0x7fa48f804d90>
However, this will remove all items currently being held by your cache
    c.cache_type.queue.to_list()
    []
####Note:
When you use queu based behaviors like MRU and LRU, the cache map holds items like
{key: IndexedObject} The *IndexedObject* is a wrapper around your actual *value*, that stores the queue index position of that key. Based on the position the eviction order is decided if the cache gets full