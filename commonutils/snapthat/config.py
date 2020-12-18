import os

class Printable:
    def _get_attributes(self):
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and not callable(getattr(self, attr)) and not attr=='_abc_impl']



        return attributes

    def _get_dict(self):
        attributes = self._get_attributes()
        dict = {i: getattr(self, i) for i in attributes}
        return dict

    def __repr__(self):
        dict = self._get_dict()
        s = str(dict)
        return s

    def __iter__(self):
        for k, v in self._get_dict().items():
            yield  k, v



class DigitalOcean(Printable):
    endpoint_url = "https://sgp1.digitaloceanspaces.com"
    ACL = "private"
    aws_access_key_id = "I5DXUEYY3RDXRUFPJXHS"
    aws_secret_access_key = "Ic2TjXnqwAJB1hQbi2C8Lu39/qlxql5PHLADIXm80gg"
    region = "sgp1"



class Config(Printable):
    CONNECTION = "'mongodb+srv://admin:123@snapthatcluster0-jmawo.mongodb.net/snapthat'"
    DB = "snapthat"
    COLLECTION= "cloths"
    AWS_ACCESS_KEY_ID= "I5DXUEYY3RDXRUFPJXHS"
    AWS_SECRET_ACCESS_KEY= "Ic2TjXnqwAJB1hQbi2C8Lu39/qlxql5PHLADIXm80gg"
    INDEX_BUCKET= "indexes"
    INDEX_PATH= "./indexes/index.idx"
    REDIS_HOST= "174.138.121.187"
    REDIS_PASSWORD= "Qwerty12#$"
    REDIS_PORT= "6379"
    CLOTH_URI= "https://www.snapthat.xyz/api/cloth/getclothespaged?start={0}&size={1}"
    CLOTH_URI_= "https://www.snapthat.xyz/api/cloth/getclothesall?start={0}&size={1}"
    AI_URL = "https://ai.snapthat.xyz/api/predict/imagevec"
    CLOTH_COUNT_URI = "https://www.snapthat.xyz/api/cloth/getcount"
    GENDER_HOST = "139.59.54.148"
    IMAGE_RETRIEVAL_HOST = "139.59.49.109"
    IMAGE_RETRIEVAL_MODELNAME = "resnet_encoder_inter"
    IMAGE_RETRIEVAL_VERSION = 1
    IMAGE_SIZE = 128
    EMBEDDING_SIZE = 128
    CLOSEST_TOP_K = 10
    BATCH_SIZE = 10
    DIGITAL_OCEAN = DigitalOcean()


class MongoConfig(Printable):
    HOST = 'localhost'
    PORT = 27017
    DATABASE = 'test'
    USERNAME = None
    PASSWORD = None
    AUTHSOURCE = 'root'

class MongoPoductionConfig(MongoConfig):
    HOST = "a8fe1206c092511eab2b60a1835f0bf3-2138289406.ap-south-1.elb.amazonaws.com"
    DATABASE =  "snapthat"
    USERNAME = "admin"
    PASSWORD = "Qwerty12"
    AUTHSOURCE = "snapthat"


class AWSS3(Printable):
    endpoint_url = "https://s3.ap-south-1.amazonaws.com"
    ACL = "private"
    aws_access_key_id =  os.getenv('AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key =  os.getenv('AWS_SECRET_ACCESS_KEY', None)
    region = "ap-south-1"
    expiration = 3  # hours

