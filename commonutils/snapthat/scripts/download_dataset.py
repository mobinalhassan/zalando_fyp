

from snapthat.datasets.cloud_downloader import CloudFileDownloader
from argparse import ArgumentParser, Namespace
from snapthat.utils import get_logger
from snapthat.cloud.storage.service_provider import cloud_storage_service, CloudStorageServiceKeys
from snapthat.config import AWSS3

logger = get_logger("Dataset Download")

aws_access_key_id = "AKIAV44TK2KFG2IRHL7V"
aws_secret_access_key = "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"

def main(args):
    """

    Args:
        args (Namespace):  args from the arg parser

    Returns:

    """
    dataset = args.dataset
    destination_directory = args.destination_directory

    s3_config = AWSS3()

    # Not recommended. pass AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY through ENV variables
    s3_config.aws_access_key_id =  args.aws_access_key_id
    s3_config.aws_secret_access_key = args.aws_secret_access_key
    # Optional
    # s3_config.endpoint_url = <aws s3 endpoint> # see https://docs.aws.amazon.com/general/latest/gr/rande.html
    # s3_config.region= <s3 region> # see https://docs.aws.amazon.com/general/latest/gr/rande.html
    # s3_config.expiration = <expiration in hours>  # public url expiration time

    s3_config = dict(s3_config)

    s3 = cloud_storage_service.get(CloudStorageServiceKeys.AWS, "snapthat-datasets", **s3_config)

    downloader = CloudFileDownloader(destination_directory, s3)
    csvs = f"{dataset}/csvs"
    images = f"{dataset}/images"
    downloader.download_directory(csvs)
    downloader.download_directory(images)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("dataset", type=str, help=f"dataset name in cloud storage bucket")
    parser.add_argument("destination_directory", type=str, help=f"the destination directory path for the dataset")
    parser.add_argument("--aws_access_key_id", type=str, help=f"cloud storage access key id", default=aws_access_key_id)
    parser.add_argument("--aws_secret_access_key", type=str, help=f"cloud storage aws_secret_access_key", default=aws_secret_access_key)

    args = parser.parse_args()
    logger.info(f"Passed Arguments: {str(args)}")
    main(args)

