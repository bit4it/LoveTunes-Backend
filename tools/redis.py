import redis


class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        value = self.redis_client.get(key)
        if value:
            return value.decode('utf-8')
        return None
    
    def set(self, key, value, ttl=-1):
        self.redis_client.set(key, value, ex=ttl)


redis_client = RedisClient()
