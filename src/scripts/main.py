import glob
import os
from src.utils import get_full_path
if __name__ == "__main__":
    try:
        if not os.path.exists(get_full_path("../data/jsons/subcat_links.json")):
            from src.scripts import get_subcat_pro_links
            get_subcat_pro_links.main()
        if not os.path.exists(get_full_path("../data/jsons/dataset.json")):
            from src.scripts import get_subcat_pro_description
            get_subcat_pro_description.main()
        if not len(glob.glob(get_full_path('../data/images'))) > 5:
            from src.scripts import images_downloader
            images_downloader.main()

        print('Done Successful !!!')
    except:
        raise Exception('Error! in main.py!!!')

