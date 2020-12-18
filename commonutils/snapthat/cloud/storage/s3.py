import boto3
from botocore.client import Config
import requests
from io import BytesIO
from snapthat.cloud.storage.storageI import CloudStorageInterface
from snapthat.cloud.storage.model import FileDataModel


class S3Storage(CloudStorageInterface):
    def __init__(self, bucket,  aws_access_key_id, aws_secret_access_key, region='sgp1',
                 endpoint_url="https://sgp1.digitaloceanspaces.com",ACL = 'private',
                 expiration=3):
        """this class deals with a single bucket per instance.
        if a bucket does not exists then the instance will try to create it


        Args:
            expiration (int): public url expiration in hours
            bucket: the bucket name.
            aws_access_key_id: get it at https://cloud.digitalocean.com/account/api/tokens
            aws_secret_access_key: get it at https://cloud.digitalocean.com/account/api/tokens
            region: storage region NYC3, AMS3, SFO2, and SGP1
            endpoint_url: digital ocean spaces endpoint
            ACL(str): 'private'|'public-read'|'public-read-write'|'authenticated-read'
        """
        self.client = None
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.region = region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.ACL = ACL
        self.expiration = expiration

        self.create_bucket()



    def get_client(self):
        if self.client is None:
            session = boto3.session.Session()
            client = session.client('s3',
                                    region_name=self.region,
                                    endpoint_url=self.endpoint_url,
                                    aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key)

            self.client = client

        return self.client

    def download_file(self, filename, destination_path, callback=None):
        client = self.get_client()
        client.download_file(self.bucket, filename, destination_path, Callback=callback)

    def upload_file(self, filename , source_path):
        client = self.get_client()
        client.upload_file(source_path, self.bucket, filename)
        client.put_object_acl(ACL=self.ACL, Bucket=self.bucket, Key=filename)


    def _list_files(self, prefix='', continuation_token= None, max_files=1000):
        client = self.get_client()

        if continuation_token is not None:
            objects = client.list_objects_v2(Bucket=self.bucket, Prefix=prefix,
                                          ContinuationToken= continuation_token, MaxKeys=max_files)
        else:
            objects = client.list_objects_v2(Bucket=self.bucket, Prefix=prefix,
                                             MaxKeys=max_files)

        contents = objects.get("Contents",[])
        files = [i for i in contents if i["Key"][-1] != "/"]
        fileobjs  = []
        for file in files:
            fileobj = FileDataModel()
            fileobj.filename = file["Key"]
            fileobj.size = file["Size"]
            fileobj.last_modified = file["LastModified"]
            fileobjs.append(fileobj)
        # filenames = [i['Key'] for i in contents if i["Key"][-1] != "/"]
        truncated = objects.get("IsTruncated", False)
        next_continuation_token = None
        if truncated:
            next_continuation_token = objects.get("NextContinuationToken", None)

        return fileobjs, next_continuation_token



    def list_files(self, prefix='', batch_size=1000):
        continuation_token = None
        while True:
            filenames, token = self._list_files(prefix=prefix, continuation_token=continuation_token,
                                                max_files=batch_size)
            yield filenames

            if token is None:
                break
            continuation_token = token


    def list_buckets(self):
        client = self.get_client()
        response = client.list_buckets()
        bucket_names = [space['Name'] for space in response['Buckets']]
        return bucket_names

    def create_bucket(self):
        client = self.get_client()
        if not self.bucket_exists():
            print("Creating new bucket...")
            client.create_bucket(Bucket=self.bucket)


    def bucket_exists(self):
        bucket_names = self.list_buckets()

        bucket = self.bucket

        exists = bucket in bucket_names

        return exists

    def delete_bucket(self, areyousure):
        if areyousure != True:
            print("please pass in true as a param to actually delete this bucket")
            return
        client = self.get_client()
        if self.bucket_exists():
            response = client.delete_bucket(Bucket=self.bucket)
            print(response)

    def get_public_url(self, filename):
        client = self.get_client()
        expire_in = self.expiration * 60 * 60  # in seconds
        url = client.generate_presigned_url('get_object', Params={'Bucket': self.bucket, 'Key': filename},
                                        ExpiresIn=expire_in)
        return url

    def upload_from_url(self, filename, url):
        r = requests.get(url, stream=True)
        status_code = r.status_code
        if status_code != 200:
            msg = str(r.text)
            max_msg_len = 200
            msg = msg if len(msg) <= max_msg_len else msg[:max_msg_len] + "..."
            raise Exception(f"Unable to locate uri, returned code {status_code} \n Response: {msg}")

        byte_obj = BytesIO(r.content)
        client = self.get_client()
        client.upload_fileobj(byte_obj, self.bucket, filename)
        client.put_object_acl(ACL=self.ACL, Bucket=self.bucket, Key=filename)

    def upload_from_stream(self, filename, streamobj):
        client = self.get_client()
        streamobj.seek(0)
        client.upload_fileobj(streamobj, self.bucket, filename)
        client.put_object_acl(ACL=self.ACL, Bucket=self.bucket, Key=filename)


    def get_size(self, key):
        client = self.get_client()
        file_object= client.get_object(Bucket=self.bucket, Key=key)
        filesize = file_object["ContentLength"]
        return filesize

    def get_last_modified(self, key):
        client = self.get_client()
        file_object= client.get_object(Bucket=self.bucket, Key=key)
        last_modified = file_object["ContentLength"]
        return last_modified

    def get_file_type(self, key):
        client = self.get_client()
        file_object= client.get_object(Bucket=self.bucket, Key=key)
        content_type = file_object["ContentType"]
        return content_type






# aws_access_key_id='AKIAV44TK2KFG2IRHL7V'
# aws_secret_access_key=''
# bucket = 'crawled-images'
#
# spaces = S3Storage(bucket,aws_access_key_id,aws_secret_access_key, 'ap-south-1',
#                    endpoint_url='https://s3.ap-south-1.amazonaws.com')
# buckets = spaces.list_buckets()
# print(buckets)
#
# filenames = spaces.list_files()
# print(filenames)

# spaces.upload_file("barny.jpg", "/home/firefrog/Pictures/barny.jpg")

# print(spaces.get_public_url('barny.jpg'))

#spaces.upload_from_url('test.jpg' , 'https://age.shutterstock.com/z/stock-photo-colorful-hot-air-balloons-flying-over-mountain-at-dot-inthanon-in-chiang-mai-thailand-1033306540.jpg')
# print(spaces.bucket_exists())
#
# # spaces.upload_file('hello.txt', './hello.txt')
# spaces.download_file("hello.txt",'./hell.txt')
# # spaces.delete_bucket(True)