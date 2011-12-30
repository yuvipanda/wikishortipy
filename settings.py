from werkzeug.contrib.cache import MemcachedCache

CACHE = MemcachedCache(['127.0.0.1:11211'])
