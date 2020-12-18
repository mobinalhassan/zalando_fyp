from snapthat.utils import  get_logger
from snapthat.cloud.storage.storageI import CloudStorageInterface
from snapthat.cloud.storage.model import FileDataModel
import os
from tqdm import tqdm
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed

from multiprocessing.pool import ThreadPool

from collections import Iterable


class CloudFileDownloader:
    def __init__(self, destination_directory, cloudstorage):
        """ Given a directory in the bucket downloads the entire content of the
        directory in to the destination directory
        Args:
            destination_directory (str): the destination directory for the dataset
            cloudstorage (CloudStorageInterface): cloud storage object for the dataset bucket

        """
        self.cloudstorage = cloudstorage
        self.destination_directory = destination_directory
        self.logger = get_logger("CloudFileDownloader")
        pass

    def _download_file(self, key, destination_path, callback=None):
        self.cloudstorage.download_file(key, destination_path, callback=callback)

    def _build_destination_file_path(self, file_key):
        """Builds the destination file path from the provided file key

        Returns:
            str: the destination file path

        """
        file_dir = self.destination_directory
        prefix = os.path.dirname(file_key)
        file_name = os.path.basename(file_key)
        file_dir = os.path.join(file_dir, prefix)

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = os.path.join(file_dir, file_name)
        return file_path

    def _download_wrap(self, fileobj, callback):
        try:
            destination_path = self._build_destination_file_path(fileobj.filename)
            self._download_file(fileobj.filename, destination_path, callback=callback)
        except Exception as ex:
            msg = str(ex)
            self.logger.error(msg)
        return fileobj

    def _calculate_total_file_sizes(self, files):
        """Calcualtes the total size of list of files
        Args:
            files (list[FileDataModel]): list of file data models

        Returns:
            int: total files size in bytes
        """
        total = 0
        for file in files:
            total += file.size
        return total

    def _extract_remaining_files(self, fileobjs):
        """images that have not already been downloaded

        Args:
            fileobjs (list[FileDataModel]): list of file data objects for images

        Returns:
            list[FileDataModel]: returns a list file data models

        """
        remaining = []
        for image_file in fileobjs:
            file_key = image_file.filename
            file_path = self._build_destination_file_path(file_key)
            if not os.path.exists(file_path):
                remaining.append(file_path)
        return remaining

    def _list_directory(self, directory_key):
        """lists the files in a bucket directory
        Args:
            directory_key (str): the directory prefix in a bucket

        Returns:
            Iterable[list[FileDataModel]]: returns a iterable of type FileDataModel in the bucket directory
        """
        for filenames in self.cloudstorage.list_files(prefix=directory_key):
            yield filenames

    def _generate_batches(self, file_data_models, batch_size):
        """Generates a list of batches for file models

        Args:
            batch_size (int):  the batch size d
            keys (list[FileDataModel]): a list of file data models

        Returns:
            list[list[FileDataModel]]: returns the generated models with len nfile_data_model/batchsize

        """
        batches = []
        no_batches = int(len(file_data_models) / batch_size)
        no_batches = no_batches if len(file_data_models) % batch_size == 0 else no_batches + 1
        for batch in range(no_batches):
            start = batch * batch_size
            end = start + batch_size
            selected = file_data_models[start:end]
            batches.append(selected)
        return batches

    def _download_files(self, file_objs, pool=None, workers = 100, seq=0, batch_no=0):
        """Downloads the given list of files

        Args:
            file_objs[list[FileDataModel]]: list of file data models
            pool: (Optional) Pass an optional thread pool

        Returns:
            None: downloads the files to the destination directory
        """
        progress_callback = lambda t: lambda bytes: t.update(bytes)
        total_size = self._calculate_total_file_sizes(file_objs)
        our_pool = False

        if pool is None:
            pool = ThreadPool(workers)
            our_pool = True

        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Seq {seq + 1} Batch {batch_no}") as t:
            callbacks = [progress_callback(t)] * len(file_objs)
            args = zip(file_objs, callbacks)
            for image_file in pool.starmap(self._download_wrap, args):
                self.logger.debug(f"Downloaded {image_file.filename} ...")
        if our_pool:
            pool.join()

    def download_directory(self, directory_key, workers=100):
        with ThreadPool(workers) as pool:
            for seq , file_objs in enumerate(self._list_directory(directory_key)):
                self.logger.info(f"Sequence {seq + 1}")
                batches = self._generate_batches(file_objs, workers)
                for batch_no, batch in enumerate(batches):
                    no_batches = len(batch)
                    self.logger.info(f"Total batches in seq {seq + 1}: {no_batches} ")
                    remaining = self._extract_remaining_files(batch)
                    total_files_in_batch = len(batch)
                    total_file_remaining_in_batch = len(remaining)
                    self.logger.info(f"Total files in batch: {total_files_in_batch} "
                                     f"Remaining: {total_file_remaining_in_batch}")

                    if total_file_remaining_in_batch == 0:
                        self.logger.info(f"Batch {batch_no} already done in sequence {seq+1}")
                        continue

                    self._download_files(batch, pool, seq=seq, batch_no=batch_no)


# from snapthat.cloud.storage.service_provider import cloud_storage_service, CloudStorageServiceKeys
# from snapthat.config import AWSS3
# s3_config= AWSS3()
#
# # Not recommended. pass AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY through ENV variables
# s3_config.aws_access_key_id = "AKIAV44TK2KFG2IRHL7V"
# s3_config.aws_secret_access_key = "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"
# # Optional
# # s3_config.endpoint_url = <aws s3 endpoint> # see https://docs.aws.amazon.com/general/latest/gr/rande.html
# # s3_config.region= <s3 region> # see https://docs.aws.amazon.com/general/latest/gr/rande.html
# # s3_config.expiration = <expiration in hours>  # public url expiration time
#
# s3_config = dict(s3_config)
#
# s3 = cloud_storage_service.get(CloudStorageServiceKeys.AWS,  "snapthat-datasets", **s3_config)
#
# image_dataset = ImageDatasetBase("/home/firefrog/dataset2", s3)
# image_dataset.download_directory("nelly/csvs")