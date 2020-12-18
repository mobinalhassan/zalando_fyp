from snapthat.builder import ServiceBuilder
from snapthat.config import MongoConfig
from snapthat.database.clients.db_mongo import PyMongoClient


class MongoClientBuilder(ServiceBuilder):
    def __init__(self, MongoConfigClass):
        """

        Args:
            MongoConfigClass (type[MongoConfig]): mongo config class
        """
        super().__init__()
        self.MongoConfigClass = MongoConfigClass

    def build(self, collection, **kwargs):
        mongo_config = self.MongoConfigClass()
        obj = PyMongoClient(collection, mongo_config.DATABASE,
                            mongo_config.HOST, mongo_config.PORT,
                            username=mongo_config.USERNAME, password=mongo_config.PASSWORD,
                            authSource=mongo_config.AUTHSOURCE)

        return obj

