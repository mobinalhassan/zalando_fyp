import json
import threading
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from src.utils import get_full_path
from src.preprocessor.parser import Parser
from src.scripts.model import filter_field_model, key_list

# for head less approch
options = Options()
options.add_argument("--hide-scrollbars")
options.add_argument("--no-sandbox")
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-impl-side-painting")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-seccomp-filter-sandbox")
options.add_argument("--disable-breakpad")
options.add_argument("--disable-client-side-phishing-detection")
options.add_argument("--disable-cast")
options.add_argument("--disable-cast-streaming-hw-encoding")
options.add_argument("--disable-cloud-import")
options.add_argument("--disable-popup-blocking")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-session-crashed-bubble")
options.add_argument("--disable-ipv6")
options.add_argument("--allow-http-screen-capture")
options.add_argument("--start-maximized")

prefs = {
    "translate_whitelists": {"fr": "en", "de": "en", 'it': 'en', 'no': 'en', 'es': 'en', 'sv': 'en', 'nl': 'en',
                             'da': 'en', 'pl': 'en', 'fi': 'en', 'cs': 'en'},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)

with open(get_full_path('../data/jsons/subcat_links.json')) as json_file:
    pro_links_list = json.load(json_file)
print(f"Length of products link ==> {len(pro_links_list)}")


class ProductDescriptionGetter:
    clothes_list = []

    def __init__(self, record):
        self.pro_url = record['source']
        self.parser = Parser()
        self.product = filter_field_model.copy()
        self.product['source'] = record['source']
        self.product['crawling_source_url'] = record['crawling_source_url']
        self.product['thumbnail'] = record['thumbnail']
        self.product['gender'] = record['gender']
        self.product['category'] = record['category']
        self.product['subcategory'] = record['subcategory']
        self.driver = webdriver.Chrome(options=options)

    def __del__(self):
        print("Delete")

    def start(self):
        print('Start')
        self.get_pro_desc()

    def save_json_file(self):
        self.clothes_list.append(self.product.copy())
        dataframe2 = pd.DataFrame(self.clothes_list)
        dataframe2.to_json(get_full_path("../data/jsons/dataset.json"), orient='records')
        print(f'File saved! Records ==> {len(self.clothes_list)}')

    def get_pro_title(self):
        try:
            title_pro: WebElement = self.driver.find_element_by_css_selector('h1').text
            title_pro_str = str(str(title_pro).strip().lower())
            self.product['title'] = title_pro_str
            # self.product['prodId'] = title_pro_str
            print(f"Product title ==> {title_pro_str}")
        except Exception as error:
            print(f"Error! in getting pro Title ==> {error}")
            self.driver.quit()
            self.__del__()

    def get_pro_price(self):
        try:
            price_raw: WebElement = self.driver.find_element_by_css_selector('div.vSgP6A._7ckuOK').text
            price = int(float(str(price_raw).split('£')[1].split('VAT')[0]))
            self.product['price'] = int(price)
            print(f"Product price ==> {price}")
            print(f"Product Currency ==> {self.product['currency']}")
        except Exception as error:
            print(f"Error! in getting Price and currency {error}")

    def get_pro_color(self):
        try:
            color_raw: WebElement = self.driver.find_element_by_css_selector('.hPWzFB span.dgII7d').text
            color = str(str(color_raw).strip().lower())
            self.product['colors'] = color
            print(f"Product color ==> {color}")
        except Exception as error:
            print(f"Error! in getting Color {error}")

    def get_pro_photos(self):
        try:
            other_pic_list = []
            product_gallery = self.driver.find_element_by_css_selector('div.WzZ4iu')
            product_gallery_source_code = product_gallery.get_attribute("innerHTML")
            product_gallery_soup: BeautifulSoup = BeautifulSoup(product_gallery_source_code, 'html.parser')
            for pro_link_for in product_gallery_soup.findAll('img'):
                try:
                    other_pic = pro_link_for['src']
                    slashparts = other_pic.split('?')
                    other_pic_list.append(slashparts[0])
                except KeyError as error:
                    print(error)
            rd_other_pic_list = list(dict.fromkeys(other_pic_list))
            self.product['otherpics'] = rd_other_pic_list
            print(f"Product Photos list ==> {rd_other_pic_list}")
        except Exception as error:
            print(f"Error! in getting Photos list {error}")

    def infinatescroll(self):
        try:
            sleep(2)
            self.driver.execute_script("window.scrollTo(0, 600)")
            pre = 600
            for i in range(0, 2):
                nextscr = pre + 600
                pre = pre + 600
                self.driver.execute_script(f"window.scrollTo({pre}, {nextscr});")
                print('Scrolling Down...')
                # Wait to load page
                sleep(1)
        except Exception as e:
            print('Error in scrolling : ' + str(e))

    def get_filter_fields(self):
        try:
            raw_html = self.driver.execute_script("return document.body.innerHTML;")
            raw_html_soup: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
            p_tags_raw = raw_html_soup.select('p[as="p"]')[:-3]
            for single_p in p_tags_raw:
                p_tag_string = str(single_p.get_text(' ').encode('ascii', 'ignore').decode('utf-8')).lower()
                for key in key_list:
                    if p_tag_string.find(f'{key}:') is not -1:
                        if p_tag_string.split(f"{key}:")[0] == '' and self.product[key] == '':
                            print(f'{key} <= key Match in text => {p_tag_string}')
                            print(f'value = {p_tag_string.split(f"{key}:")[-1].strip()}')
                            self.product[key] = p_tag_string.split(f"{key}:")[-1].strip()
                            print('*' * 150)

        except Exception as error:
            print(f"Error in getting Filter fields ==> {error}")

    def get_pro_desc(self):
        try:
            print(f"Getting Desc for URL ==> {self.pro_url}")
            self.driver.get(self.pro_url)
            sleep(5)
            self.infinatescroll()
            self.get_pro_title()
            self.get_pro_price()
            self.get_pro_color()
            sleep(2)
            self.get_pro_photos()
            self.parser.parse_missing_value(self.product)
            print(self.product)
            self.save_json_file()
            self.driver.quit()
        except Exception as error:
            print(f"Error in getting description page ==> {error}")


def main():
    thread = 2
    for i in range(0, len(pro_links_list), thread):
        all_t = []
        twenty_records = pro_links_list[i:i + thread]
        for record_arg in twenty_records:
            try:
                pdg = ProductDescriptionGetter(record_arg)
                t = threading.Thread(target=pdg.start)
                t.start()
                all_t.append(t)
            except Exception as error:
                print(f"Error in starting thread ==> {error}")
        for count, t in enumerate(all_t):
            print(f" joining Thread no ==> {count}")
            t.join()
        break


if __name__ == "__main__":
    main()
