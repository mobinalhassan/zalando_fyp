import pandas as pd
from snapthat.image.image_downloader import image_downloader
import os
import json
from src.utils import get_full_path


class Downloader:
    def __init__(self):
        os.makedirs(get_full_path("../data/images/"), exist_ok=True)
        self.data_path = get_full_path("../data/jsons/dataset.json")
        self.destination_dir = get_full_path("../data/images/")
        self.batch_size = 500
        self.parallel_workers = 10
        self.data_for_df = []
        self.image_path_file_df = []
        self.start_batch = 0

    def start(self):
        self.make_dataframe()
        self.run()

    def save_file(self):
        os.makedirs(get_full_path("../data/csvs/"), exist_ok=True)
        pd.DataFrame(self.image_path_file_df).to_csv(get_full_path('../data/csvs/images_path_file.csv'),
                                                     index=False)

    def make_dataframe(self):
        count = 0
        with open(self.data_path, 'r') as file_json:
            for record_index, data in enumerate(iter(json.load(file_json))):
                data_df = {'filenames': '', 'urls': ''}
                filename = f'{record_index}_thum'
                # filename = f'{record_index}'
                data_df['filenames'] = filename
                if data['thumbnail'].find('http') == -1 and data['thumbnail']:
                    data['thumbnail'] = 'https://' + data['thumbnail']
                data_df['urls'] = data['thumbnail']
                if len(data_df['urls']):
                    self.data_for_df.append(data_df)
                    print(data_df)
                    print('=' * 75)
                    image_path_file = {'index': '', 'filename': '', 'url': '', 'colors': data['colors'],
                                       'category': data['category'],
                                       'subcategory': data['subcategory'],
                                       'gender': data['gender']}
                    folder_num = int(count / self.batch_size)
                    count = count + 1
                    image_path_file['index'] = record_index
                    file_path = f'images/{folder_num}/{filename}'
                    image_path_file['filename'] = file_path
                    image_path_file['url'] = data['thumbnail']
                    print(image_path_file)
                    self.image_path_file_df.append(image_path_file)

                for url_index, picurl in enumerate(data['otherpics']):
                    data_df = {'filenames': '', 'urls': ''}
                    filename = f'{record_index}_{url_index}'
                    data_df['filenames'] = filename
                    if picurl.find('http') == -1 and picurl != '':
                        picurl = 'https://' + picurl
                    data_df['urls'] = picurl
                    if len(data_df['urls']):
                        self.data_for_df.append(data_df)
                        print(data_df)
                        print('=' * 75)
                        image_path_file = {'index': '', 'filename': '', 'url': '', 'colors': data['colors'],
                                           'category': data['category'],
                                           'subcategory': data['subcategory'],
                                           'gender': data['gender']}
                        folder_num = int(count / self.batch_size)
                        count = count + 1
                        image_path_file['index'] = record_index
                        file_path = f'images/{folder_num}/{filename}'
                        image_path_file['filename'] = file_path
                        image_path_file['url'] = picurl
                        print(image_path_file)
                        self.image_path_file_df.append(image_path_file)

        self.save_file()

    def run(self):
        data_give = pd.DataFrame(self.data_for_df)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
        }
        image_downloader(data_give, self.destination_dir, self.start_batch, batch_size=self.batch_size,
                         workers=self.parallel_workers, headers=headers)


def main():
    downloader = Downloader()
    downloader.start()


if __name__ == "__main__":
    main()
