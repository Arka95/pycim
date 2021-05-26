import threading

class Singleton(type):
    # TODO: move this to a separate file
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Policy:
    # TODO: move writeback fallbacks inside a background service
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"

def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return bg_f