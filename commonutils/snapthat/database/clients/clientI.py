from abc import ABC, abstractmethod
from pymongo.collection import Collection

class DBClientInterface(ABC):

    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    def get_database(self):
        pass

    @abstractmethod
    def get_collection(self):
        """Gets the target collection/table object

        Returns:
            Collection: returns the mongo collection object

        """
        pass

    @abstractmethod
    def list_collections(self):
        pass

    @abstractmethod
    def list_databases(self):
        pass
