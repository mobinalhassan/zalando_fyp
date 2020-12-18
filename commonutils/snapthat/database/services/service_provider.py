
from enum import Enum
from snapthat.database.services.cloth import ClothService
from snapthat.database.services.brand import BrandService
from snapthat.database.services.brand_cloth import BrandClothService
from snapthat.database.services.db_servicesI import DatabaseServiceInterface
from snapthat.factory import ObjectFactory


class DatabaseServiceKeys(Enum):
    Cloth = "Clothes Service"
    Brand = "Brand Service"
    BrandCloth = "Brand Cloth Service"



class DatabaseServiceProvider(ObjectFactory):
    def get(self, key, **kwargs):
        """gets the instantiated cloud

        Args:
            key(str): the object key
            **kwargs(dict): additional kwargs

        Returns:
            DatabaseServiceInterface: returns a database service

        """
        return self.create(key,  **kwargs)


database_service = DatabaseServiceProvider()
database_service.register_builder(DatabaseServiceKeys.Cloth, ClothService)
database_service.register_builder(DatabaseServiceKeys.Brand, BrandService)
database_service.register_builder(DatabaseServiceKeys.BrandCloth, BrandClothService)

