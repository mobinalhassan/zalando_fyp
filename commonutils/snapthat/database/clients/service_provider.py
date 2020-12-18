
from enum import Enum
from snapthat.database.clients.builder import MongoClientBuilder
from snapthat.factory import ObjectFactory
from snapthat.config import MongoConfig
from snapthat.database.clients.clientI import DBClientInterface

class DBClientServiceKeys(Enum):
    MONGO = "Mongodb python client"
    REDIS = "Redis client"


class DBClientServiceProvider(ObjectFactory):
    def get(self, key , collection, **kwargs):
        """gets the instantiated cloud

        Args:
            key(DBClientServiceKeys): the object key
            **kwargs(dict): additional kwargs

        Returns:
            DBClientInterface: return a client object of type db client interface

        """
        kwargs.update({'collection': collection})
        return self.create(key, **kwargs)


database_service = DBClientServiceProvider()
database_service.register_builder(DBClientServiceKeys.MONGO, MongoClientBuilder(MongoConfig))
