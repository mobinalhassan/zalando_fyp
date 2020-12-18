from snapthat.database.services.service_provider import database_service, DatabaseServiceKeys
from snapthat.database.models.brand_cloth import BrandClothModel

service = database_service.get(DatabaseServiceKeys.BrandCloth)
model = BrandClothModel()

res = service.count({})
print(res)


brand_service = database_service.get(DatabaseServiceKeys.Brand)
brands = brand_service.find({"brand_name": "hello"})
brand_id = str(brands[0]["_id"])
brand_name = brands[0]["brand_name"]


model.brand_id = brand_id
model.brand_name = brand_name
model.thumbnail = "nelly/images/0/0_0.jpg"
model.gender = "female"
model.title = "some random clothing item"
model.price = 5000


model.prodId="8911"
model.price = 3000

brand_cloth_id = service.add(model)
print(f"Brand Cloth id {brand_cloth_id}")


res = service.find({"_id": brand_cloth_id})
print(res)


res = service.find({},skip=0, limit=1000, sort=[('price' , 1)])
print(len(res))
print([i["price"] for i in res])
