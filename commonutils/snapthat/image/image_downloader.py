import numpy as np
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import requests
from PIL import Image
from io import BytesIO
import time

from snapthat.utils import get_filelogger, get_logger
from snapthat.networkrequests.networkutils import format_url

filelogger = get_filelogger("filedlogger")
logger = get_logger("consolelogger")


def get_filenames_urls(data, image_keys):
    """flattens the data frame containing image keys to a
    sequence of filenames and urls while generating a corresponding filename for
    each image url

    Args:
        data(pd.DataFrame): a dataframe containing image urls
        image_keys(list[str]): a list of column names containinf image urls

    Returns:
        pd.DataFrame: returns a data frame object with keys: filenames, urls, indexes
    """
    processed_data = {'filenames': [], 'urls': [], 'indexes': []}
    for i, row in data.iterrows():
        for position in image_keys:
            url = row[position]
            if url is not None:
                filename = str(i) + '_' + position + '.png'
                processed_data['filenames'].append(filename)
                processed_data['urls'].append(url)
                processed_data['indexes'].append(i)

    processed_data_df = pd.DataFrame(processed_data)
    return processed_data_df


def download_image(source_url, destination_path, timeout=10, headers=None):
    """
    Args:
        source_url(str): the source url
        destination_path(str): the full destination path
    """
    try:
        source_url = format_url(source_url)
        response = requests.get(source_url,verify=False, timeout=timeout, headers=headers)
        code = response.status_code

        if code != 200:
            txt = str(response.text)
            raise Exception(f"return code {code} response: {txt}")

        content = response.content
        buffer = BytesIO(content)
        image = Image.open(buffer)
        image = image.convert("RGB")
        image.save(destination_path, format="JPEG")
    except Exception as ex:
        msg = str(ex)
        err = f"Error at url: {source_url} Message: {msg}"
        # print(err)
        filelogger.error(err)


def download_image_concurrent(urls, destination_paths, workers=10, headers=None):
    futures = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for url, filename in zip(urls, destination_paths):
            future = ex.submit(download_image, url, filename, headers=headers)
            futures.append(future)

        as_completed(futures)


def image_downloader(dataset, destination_dir, start_batch=0, batch_size=500, workers=100, headers=None):
    """an implementation of a image downloader designed for long image dowloading tasks
    uses a concurrent pool of processes to download images in parallel. the downloader
    divides the image into directories according to the batch number so that large
    images do not create a load on the filemanger/explorer while view them manually.
    the process can be viewed through console logs or logs in the log directory.

    Args:
        dataset(pd.DataFrame): a dataframe object with keys: urls, filenames
        destination_dir(str): the destination directory
        start_batch(int): (default: 0) if specified, resumes downloading from this batch number
        batch_size(int): the number of images per batch/directory
        workers: number of parallel processes/workers

    Returns:
        None: saves the images to the specified directory

    """

    if not os.path.isdir(destination_dir):
        raise Exception('destination directory does not exists!')
    downloadList = list(zip(dataset['urls'], dataset['filenames']))
    ndownloads = len(downloadList)
    nbatches = int(ndownloads / batch_size) + 1

    logger.info(f"Destination directory: {destination_dir}")
    logger.info(f"Total downloads {ndownloads} Batches {nbatches}  batchsize {batch_size} workers {workers}")

    for batchno in range(start_batch, nbatches):
        start = batchno * batch_size
        end = start + batch_size

        destination_batch_dir = os.path.join(destination_dir, str(batchno))
        if not os.path.isdir(destination_batch_dir):
            os.makedirs(destination_batch_dir)

        sample = downloadList[start: end]
        unzip = list(zip(*sample))

        urls = unzip[0]
        filenames = unzip[1]
        destination_paths = [os.path.join(destination_batch_dir, i) for i in filenames]

        #     for i, (url, filename) in enumerate(sample):
        #         destination_path = os.path.join(destination_batch_dir, filename)
        #         download_image(url, destination_path )

        t1 = time.time()
        download_image_concurrent(urls, destination_paths, workers=workers, headers=headers)
        t2 = time.time()
        diff = (t2 - t1) / 60
        logger.info(f"Downloaded batch {batchno} took {diff} minutes")




def main():
    start_batch = 0
    destination_dir = "/home/firefrog/Pictures/fashion"
    data = {'filenames': ["test1", "test2", "test3"], 'urls': ["cdn.shopify.com/s/files/1/2160/5767/products/YELLOW_OCHRE_1024x1024.png?v=1571610450",
                                            "cdn.shopify.com/s/files/1/2160/5767/products/PD-2899_4_9fa99765-caff-4c68-99a7-a729747f93ae_1024x1024.png?v=1571610883",
                                                               "https://cdn.shopify.com/s/files/1/2160/5767/products/Maria_B_009_b_1024x1024.jpg?v=1571610553"]}
    # dataset = dataset_from_dataframe(data)
    dataset_frame = pd.DataFrame(data)
    print(dataset_frame.head())

    image_downloader(dataset_frame, destination_dir, start_batch=start_batch, batch_size=10)


if __name__ == "__main__":
    main()


