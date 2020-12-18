from snapthat.database.clients.clientI import DBClientInterface
from snapthat.database.models.brand import BrandModel

from snapthat.database.clients.service_provider import database_service, DBClientServiceKeys
from snapthat.database.services.base_service import BaseService


class BrandService(BaseService):
    def __init__(self, collection = 'brands', DataModel=BrandModel, dbengine=DBClientServiceKeys.MONGO):
        """

        Args:
            DataModel ():
        """
        super().__init__(collection, DataModel, dbengine)
        self.collection = collection
        self.dbengine = dbengine
        self.db_client = database_service.get(self.dbengine , self.collection)
        self.DataModel = DataModel

