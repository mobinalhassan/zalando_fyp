
from snapthat.resourcesync.cloudstorage_sync import CloudStorageSynchronizer
from snapthat.cloud.storage.service_provider import cloud_storage_service, CloudStorageServiceKeys
from snapthat.config import AWSS3
from datetime import timedelta

# For details on s3 cloud storage, visit the Cloud Storage Guide
s3_config= AWSS3()

# Not recommended. pass AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY through ENV variables
s3_config.aws_access_key_id = "<AWS_ACCESS_KEY_ID>"
s3_config.aws_secret_access_key = "<AWS_SECRET_ACCESS_KEY>"


destination_dir = "path/to/destination/directory"
source_bucket = "source_bucketname"
check_interval = timedelta(hours=1)  # check for new/ updated sources after this interval

s3_config = dict(s3_config)
s3 = cloud_storage_service.get(CloudStorageServiceKeys.AWS,  source_bucket, **s3_config)
synchronizer = CloudStorageSynchronizer(s3, destination_dir, synchronize_interval=check_interval)

synchronizer.register_callback(lambda: print("hello new resource synchronized"))  # register any callbacks which
# will be fired once the resource is synchronized

synchronizer.start()  # Runs asynchronously
