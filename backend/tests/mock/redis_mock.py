class RedisMock:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
        return cls._instance

    async def set(self, key, value, *args, **kwargs):
        self.data[key] = value

    async def get(self, key):
        return self.data.get(key)

    async def flushdb(self):
        self.data.clear()
