
from enum import Enum
from snapthat.cloud.storage.s3 import S3Storage
from snapthat.cloud.storage.storageI import CloudStorageInterface
from snapthat.factory import ObjectFactory
from snapthat.config import AWSS3

class CloudStorageServiceKeys(Enum):
    DO = "Digital Ocean"
    AWS = "Amazon Web Services"


class CloudStorageServiceProvider(ObjectFactory):
    def get(self, key , bucket, **kwargs):
        """gets the instantiated cloud

        Args:
            bucket (str): bucket name
            key(str): the object key
            **kwargs(dict): additional kwargs

        Returns:
            CloudStorageInterface: returns a digital ocean spaces

        """
        kwargs.update({'bucket':bucket})
        return self.create(key,  **kwargs)


cloud_storage_service = CloudStorageServiceProvider()
cloud_storage_service.register_builder(CloudStorageServiceKeys.DO, S3Storage)
cloud_storage_service.register_builder(CloudStorageServiceKeys.AWS, S3Storage)
