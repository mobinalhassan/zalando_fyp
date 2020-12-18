from snapthat.database.services.service_provider import database_service, DatabaseServiceKeys
from snapthat.database.models.cloth import ClothModel
from snapthat.config import MongoConfig


# For production database

# MongoConfig.HOST = "a8fe1206c092511eab2b60a1835f0bf3-2138289406.ap-south-1.elb.amazonaws.com"
# MongoConfig.USERNAME = "<USERNAME>"
# MongoConfig.PASSWORD = "<PASSWORD>"
# MongoConfig.AUTHSOURCE = "snapthat"
# MongoConfig.DATABASE = "snapthat"


cloth_service = database_service.get(DatabaseServiceKeys.Cloth)
res = cloth_service.count({})
print(res)


model = ClothModel()
model.title = 'yo'
model.brand_name = 'sana safinaz'
model.zoomedpics = ['yolo', 'http://molo', 'http://trollo']
model.gender = 'MALE'
model.thumbnail = 'SSSssasWQwq'
model.source = 'jkljk'
model.price = 20


# model.preprocess_and_validate()
#
# #
print(model)

res = cloth_service.add(model)  # this model can also be any dict with valid fields
returned_id = res

#
res = cloth_service.find({'_id': returned_id})
print(res)
#
#
#
model.title = 'Long Black Lawn sapphire'
#
res = cloth_service.update(returned_id, model)
print(res)  # updated count
#
res = cloth_service.remove({'_id': returned_id})
print(res)  # remove count

#
model.source = "source100"

model1 = ClothModel()
model1.update(model)
model1.source = "source101"

model2 = ClothModel()
model2.update(model)
model2.source = "source102"


# res = cloth_service.add_bulk([model, model1, model2])
# print(res)

