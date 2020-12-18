import pandas as pd

from snapthat.image.image_downloader import image_downloader


data_path = "path/to/json/or/csv/file"
destination_dir = "path/to/destination/directory"
batch_size = 500  # the batch size of each image directory
parallel_workers = 100
dataset = pd.read_csv(data_path)  # dataset must have filenames, urls columns/key. May need to rename/preprocess it

start_batch = 0  # start from batch zero or resume from a arbitrary batch number
image_downloader(dataset, destination_dir, start_batch, batch_size=batch_size, workers=parallel_workers)

