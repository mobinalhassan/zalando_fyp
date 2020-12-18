import redis

class MyRedis:
    def __init__(self, host, password, port= 6379):
        self.host = host
        self.password = password
        self.port = port
        self.client = None
        self.pattern = 'dramatiq*'

    def get_client(self):
        if self.client is None:
            client = redis.Redis(host=self.host, port = self.port, password= self.password)
            self.client = client

        return self.client


    def get_keys(self, pattern='*'):
        client = self.get_client()
        keys = client.keys(pattern)
        keys = [i.decode('utf8') for i in keys]
        return keys

    def clear_keys(self, pattern =None):
        client = self.get_client()
        if pattern is None:
            pattern = self.pattern

        keys = self.get_keys(pattern)
        for k in keys:
            client.delete(k)





