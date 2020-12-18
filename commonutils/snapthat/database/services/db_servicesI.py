from abc import ABC, abstractmethod


class DatabaseServiceInterface(ABC):

    @abstractmethod
    def get_collection(self):
        """returns the table/collection instance"""
        pass

    @abstractmethod
    def add(self, data):
        """

        Args:
            data (dict): dict compatible object

        Returns:
            str: returns the inserted id

        """

        pass

    @abstractmethod
    def find(self, query, skip=0, limit=1000, sort=None):
        """

        Args:
            query (dict): query of type dictionary

        Returns:
            list: returns a list of records

        """
        pass

    @abstractmethod
    def count(self, query):
        """

        Args:
            query (dict): query of type dictionary

        Returns:
            int: returns the count of record based on the query

        """
        pass

    @abstractmethod
    def update(self, id, data):
        """

        Args:
            id (str): id of record to update
            data (ClothModel): cloth model or dict with valid keys

        Returns:
            int: modified record count

        """

        pass

    @abstractmethod
    def add_bulk(self, data):
        """add list of cloth models

        Args:
            data (list): list of data model or dict with valid keys

        Returns:
            list[str]: returns the inserted ids

        """

        pass

    def remove(self, query):
        """removes a single record. query may include a '_id' string field
        to delete record by id

        Args:
            query (dict): a query in dictionary format

        Returns:
            int: returns the removed id

        """

        pass


