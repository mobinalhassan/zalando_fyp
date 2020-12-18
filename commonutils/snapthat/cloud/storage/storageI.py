from abc import ABC, abstractmethod
from _io import _IOBase
from snapthat.cloud.storage.model import FileDataModel
class CloudStorageInterface(ABC):

    @abstractmethod
    def download_file(self, filename, destination_path, callback=None):
        """

        Args:
            destination_path (str): destination path in local drive
            filename (str): source file name in the bucket
            callback (function): (optional) a callable object with single parameter
                for receiving bytes

        """
        pass

    @abstractmethod
    def upload_file(self, filename , source_path):
        """

        Args:
            source_path (str): source file path on local drive
            filename (str): destination filename
        """
        pass

    @abstractmethod
    def list_files(self, prefix='', batch_size=1000):
        """

        Args:
            batch_size (int): the maximum number of filenames
            prefix (str): the prefix path in bucket


        Returns:
            list[FileDataModel]: returns a list of FileDataModelObjects from bucket

        """
        pass

    @abstractmethod
    def list_buckets(self):
        """

        Returns:
            list[str]: returns a list of bucket names

        """
        pass

    @abstractmethod
    def create_bucket(self):
        """creates a new bucket on the cloud"""
        pass

    @abstractmethod
    def bucket_exists(self):
        """check if bucket exists

        Returns:
            bool: returns boolean result for existance

        """
        pass

    @abstractmethod
    def delete_bucket(self, areyousure):
        """deletes a bucket from cloud. must send true in areyousure as an
        extra added security measure

        Args:
            areyousure (bool): send true to delete bucket
        """
        pass

    @abstractmethod
    def get_public_url(self, filename):
        """Returns the public url with token of the file in the bucket
        that is accessible within a time period
        Args:
            filename (str): the file name in the bucket

        Returns:
            str: returns the public url
        """

        pass

    @abstractmethod
    def upload_from_url(self, filename, url):
        """directly uploads a file from url to bucket
        Args:
            filename (str): the destination filename in bucket
            url (str): valid string url
        """

        pass

    @abstractmethod
    def upload_from_stream(self, filename, streamobj):
        """uploads from a stream like object (can be a ByteIO object) to the cloud bucket

        Args:
            streamobj (_IOBase): stream like object. for in memory use ByteIO
            filename (str): the filename in the bucket

        """
        pass

    @abstractmethod
    def get_size(self, key):
        """get the size of the file in the bucket in bytes
        Args:
            key (str): the file path in the bucket
        Returns:
            int: the size in bytes
        """

        pass

    @abstractmethod
    def get_last_modified(self, key):
        """Gets the last modified date of the file in the bucket in bytes
        Args:
            key (str): the file path in the bucket
        Returns:
            datetime: the datetime object containing the last modified date
        """

        pass

    @abstractmethod
    def get_file_type(self, key):
        """Gets the type of the file in the bucket in bytes
        Args:
            key (str): the file path in the bucket
        Returns:
            str: the file type e.g: text/csv
        """

        pass



