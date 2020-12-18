
from snapthat.database.clients.clientI import DBClientInterface
from snapthat.database.models.cloth import AbstractDBModel

from snapthat.database.clients.service_provider import database_service, DBClientServiceKeys
from snapthat.database.services.db_servicesI import DatabaseServiceInterface
from bson.objectid import ObjectId

from snapthat.database.models.indexing import DatabaseIndex


class  BaseService(DatabaseServiceInterface):
    def __init__(self, collection, DataModel, dbengine):
        """

        Args:
            DataModel (type[AbstractDBModel]): data model class of type AbstractDBModel
            dbengine (DBClientServiceKeys): valid registered database engine key

        """
        self.collection = collection
        self.dbengine = dbengine
        self.db_client = database_service.get(self.dbengine , self.collection)
        self.DataModel = DataModel

    def get_collection(self):
        collection = self.db_client.get_collection()
        return collection


    def _get_db_indexes(self):
        collection = self.get_collection()
        index_info = collection.index_information()
        return index_info

    def _create_indexes(self):
        model = self.DataModel()
        my_indexes = model.indexes()
        db_indexes = self._get_db_indexes()
        for idx in my_indexes:
            my_index_name = idx.get_name()
            if my_index_name in db_indexes.keys():
                continue

            self._create_index(idx)

    def _create_index(self, index):
        """Creates a database index if not already exists. Checks
        if the fields exists in the model before creating an index

        Args:
            index (DatabaseIndex):
        Returns:

        """
        model = self.DataModel()
        original_fields = dict(model).keys()

        index_name = index.get_name()
        is_unique = index.is_unique()
        is_background = index.is_background()
        collection = self.get_collection()
        db_index = index.toDBIndex()

        for field in index.get_fields():
            if field not in original_fields:
                raise Exception(f"field {field} does not exists in model")

        collection.create_index(db_index, unique=is_unique, background=is_background, name=index_name)

    def add(self, data):
        """Adds the record to the collection. Tries to create missing indexes.

        Args:
            data (AbstractDBModel): model object of type AbstractDBModel or dictionary with valid keys

        Returns:
            str: returns the inserted id

        """
        self._create_indexes()
        collection = self.db_client.get_collection()

        model = self.DataModel()
        model.update(data)

        model.preprocess_and_validate()

        result = collection.insert_one(dict(model))
        id = result.inserted_id

        return str(id)

    def find(self, query, skip=0, limit=1000, sort=None):
        """

        Args:
            query (dict): query of type dictionary
            limit (int): the upper limit for returning records
            skip (int):  number of records to skip
            sort (dict): the sort query e.g {_id: -1} sort id in DESC

        Returns:

        """
        collection = self.db_client.get_collection()
        if '_id' in query:
            query['_id'] = ObjectId(query['_id'])

        result = collection.find(query)
        if sort is not None:
            result = result.sort(sort)
        result = result.skip(skip).limit(limit)

        result = list(result)
        return result

    def count(self, query):
        """

        Args:
            query (dict): query of type dictionary

        Returns:

        """
        collection = self.db_client.get_collection()
        result = collection.count_documents(query)
        return result

    def update(self, id, data):
        """

        Args:
            id (str): id of record to update
            data (object[AbstractDBModel]): AbstractDBModel object or dict with valid keys

        Returns:
            int: modified record count

        """

        collection = self.db_client.get_collection()
        id =  ObjectId(id)

        rows = self.find({'_id': id})
        if len(rows) == 0:
            raise Exception(f'No record found with id {id}')

        row = rows[0]
        row = dict(row)

        model = self.DataModel()
        model.update(row)
        model.update(data)

        model.preprocess_and_validate()

        res = collection.update_one({'_id': id}, {'$set': dict(model)})
        count = res.modified_count

        return count

    def add_bulk(self, data):
        """add list of cloth models

        Args:
            data (list): list of data model or dict with valid keys

        Returns:
            list[str]: returns the inserted ids

        """
        assert  isinstance(data, list), f"data must be a list, give: {data}"
        self._create_indexes()

        collection = self.db_client.get_collection()

        rows = [self.DataModel().update(row).preprocess_and_validate() for row in data]
        rows = [dict(row) for row in rows if row.is_valid()]

        if len(rows) == 0:
            raise Exception("No valid models to add")

        result = collection.insert_many(rows)
        ids = [str(id) for id in result.inserted_ids]

        return ids


    def remove(self, query):
        """removes a single record. query may include a '_id' string field
        to delete record by id

        Args:
            query (dict): a query in dictionary format

        Returns:
            int: returns the removed id

        """

        collection = self.db_client.get_collection()

        if '_id' in query:
            query['_id'] = ObjectId(query['_id'])

        result= collection.delete_one(query)
        return result.deleted_count


