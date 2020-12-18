from snapthat.database.services.service_provider import database_service, DatabaseServiceKeys
from snapthat.database.models.brand_cloth import BrandClothModel
from snapthat.database.models.brand import BrandModel


brand_service = database_service.get(DatabaseServiceKeys.Brand)

model = BrandModel()
model.brand_name = "hello"

res = brand_service.add(model)
print(res)