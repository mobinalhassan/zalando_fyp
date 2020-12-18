
from pymongo import MongoClient
from snapthat.database.clients.clientI import DBClientInterface
from pymongo.collection import Collection



class PyMongoClient(DBClientInterface):
    def __init__(self, collection, database='test', host='localhost', port=27017,
                 username=None, password=None, authSource = None):
        self.database = database
        self.collection = collection
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.authSource = authSource
        self.client = None
        pass

    def get_client(self):
        if self.client is not None:
            return self.client

        client = MongoClient(self.host, self.port,  username = self.username,
                             password=self.password, authSource= self.authSource)
        self.client = client

        return self.client

    def get_database(self):
        client = self.get_client()
        db = client[self.database]
        return db


    def get_collection(self):
        """Gets the target collection object

        Returns:
            Collection: returns the mongo collection object

        """
        db = self.get_database()
        collection = db[self.collection]
        return collection


    def list_collections(self):
        db = self.get_database()
        collection_names = db.list_collection_names()
        return collection_names

    def list_databases(self):
        client = self.get_client()
        database_names = client.list_database_names()
        return database_names



# c = PyMongoClient("test_collection",  "test1")
# print(c.list_databases())
# print(c.list_collections())