import logging

# logging.getLogger().setLevel(logging.INFO)

# from application_context import dospace_indexes
from snapthat.cloud.storage.storageI import CloudStorageInterface
from datetime import datetime, timedelta
from snapthat.utils import get_full_path, get_logger
import os
import time

import threading


class CloudStorageSynchronizer:
    def __init__(self, cloud_storage, destination_dir, synchronize_interval=timedelta(hours=0.5)):
        """Synchronizes resource to local directory from cloud storage.
        the cloud storage instance should have set bucket context. all sync ops will
        be executed in the context of the bucket

        Args:
            cloud_storage (CloudStorageInterface): object instance of type Cloud storage interface.
            destination_dir (str): the destination directory to synchronize to
        """
        self.cloud_storage = cloud_storage
        self.destination_dir = destination_dir
        self.watch_list = None
        self.watch_list_update = timedelta(hours=1)
        self.watch_list_last_updated = None

        self.last_synchronized = None
        self.synchronize_interval = synchronize_interval

        self.callback_funcs = []
        self.callback_args = []
        self.logger = get_logger("ResourceSynchronizer", level=logging.INFO)



    def get_watch_list(self):
        last_updated = self.watch_list_last_updated
        if last_updated is None:
            last_updated = datetime.utcnow()

        update_diff = datetime.utcnow() - last_updated

        if self.watch_list is None or len(self.watch_list)==0 or update_diff >= self.watch_list_update:
            filenames= self.cloud_storage.list_files()
            self.watch_list = filenames
            self.watch_list_last_updated = datetime.utcnow()

        return self.watch_list

    def synchronize(self):
        while True:
            time.sleep(2)
            try:
                now = datetime.utcnow()
                if self.last_synchronized is None:
                    self.last_synchronized = now

                interval_diff = now - self.last_synchronized

                if interval_diff != timedelta() and interval_diff <= self.synchronize_interval:
                    self.logger.debug(f"Too early to synchronize. sleeping...")
                    continue

                watch_list = self.get_watch_list()

                for filename in watch_list:
                    filepath = os.path.join(self.destination_dir, filename)
                    self.logger.info(f"downloading into {filepath} ...")
                    self.cloud_storage.download_file(filename, filepath)

                self.logger.info(f"finished downloading...")
                self._call_callbacks()

                self.last_synchronized = datetime.utcnow()
            except Exception as ex:
                msg = str(ex)
                self.logger.exception(msg)

    def start(self):
        sync_t = threading.Thread(target=self.synchronize)
        sync_t.start()


    def register_callback(self, callback_func, **kwargs):
        self.callback_funcs.append(callback_func)
        self.callback_args.append(kwargs)

    def _call_callbacks(self):
        for callback_func , kwargs in zip(self.callback_funcs, self.callback_args):
            try:
                callback_func(**kwargs)
            except Exception as ex:
                msg = str(ex)
                self.logger.exception(msg)


# def sample():
#     print("callback called after downloading...")
#
# def sample2():
#     print("sample 2 printing")
# rs = ResourceSynchronizer(dospace_indexes, get_full_path('indexes'),synchronize_interval=timedelta(minutes=0.5))
# rs.register_callback(sample)
#
# rs.start()

# print("after start")
# time.sleep(20)
# rs.register_callback(sample2)




