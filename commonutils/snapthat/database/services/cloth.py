
from snapthat.database.clients.clientI import DBClientInterface
from snapthat.database.models.cloth import ClothModel, AbstractDBModel

from snapthat.database.clients.service_provider import database_service, DBClientServiceKeys
from snapthat.database.services.base_service import BaseService
from bson.objectid import ObjectId


class ClothService(BaseService):
    def __init__(self, collection = 'cloths', DataModel=ClothModel, dbengine=DBClientServiceKeys.MONGO):
        """

        Args:
            datamodel:
        """
        super().__init__(collection, DataModel, dbengine)
        self.collection = collection
        self.dbengine = dbengine
        self.db_client = database_service.get(self.dbengine , self.collection)
        self.DataModel = DataModel




# model = ClothModel()
# model.title = 'yo'
# model.brand_name = 'sana safinaz'
# model.zoomedpics = ['yolo', 'http://molo', 'http://trollo']
# model.gender = 'MALE'
# model.frontpic = 'ldkl'
# model.source = 'jkljk'
# model.price = 20
#
# print(model)


#
# clothService = ClothService()
# res = clothService.add(model)
# print(res)

# res = clothService.find({'_id': '5df14b734c1e0e4d0c4bc686'})
# print(res)
#
# res = clothService.add_bulk([model, model, model])
# print(res)
#
# res = clothService.count({})
# print(res)
# #
# res = clothService.update('5df14b734c1e0e4d0c4bc686', model)
# print(res)
#
#
# res = clothService.remove({'_id': '5df14b734c1e0e4d0c4bc686'})
# print(res)

