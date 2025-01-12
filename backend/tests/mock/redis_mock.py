import time


class RedisMock:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
            cls._instance.expires = {}
        return cls._instance

    async def set(self, key, value, *args, **kwargs):
        self.data[key] = value
        if "ex" in kwargs:
            self.expires[key] = time.time() + kwargs["ex"]

    async def setex(self, key, seconds, value):
        self.data[key] = value
        self.expires[key] = time.time() + seconds

    async def get(self, key):
        if key in self.expires:
            if time.time() > self.expires[key]:
                del self.data[key]
                del self.expires[key]
                return None
        return self.data.get(key)

    async def ttl(self, key):
        if key not in self.expires:
            return -1
        remaining = int(self.expires[key] - time.time())
        if remaining <= 0:
            del self.data[key]
            del self.expires[key]
            return -2
        return remaining

    async def flushdb(self):
        self.data.clear()
        self.expires.clear()

    async def delete(self, key: str) -> int:
        existed = 0
        if key in self.data:
            del self.data[key]
            existed = 1
        if key in self.expires:
            del self.expires[key]
        return existed
