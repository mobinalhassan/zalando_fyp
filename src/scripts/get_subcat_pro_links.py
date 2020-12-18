import json
import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.utils import get_full_path
from src.scripts.subcat_links_list import subcat_link_list

options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument('--no-sandbox')
options.add_argument("--hide-scrollbars")
options.add_argument("disable-infobars")
options.add_argument('--disable-dev-shm-usage')
prefs = {
    "translate_whitelists": {"fr": "en", "de": "en", 'it': 'en', 'no': 'en', 'es': 'en', 'sv': 'en', 'nl': 'en',
                             'da': 'en', 'pl': 'en', 'fi': 'en', 'cs': 'en'},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)


class ProductLinksGetter:
    pro_links_list = []

    def __init__(self, record):
        self.web_url = record['url']
        self.gender = record['gender']
        self.category = record['category']
        self.subcategory = record['subcategory']
        self.driver = webdriver.Chrome(options=options)

    def start(self):
        print('start')
        self.get_pro_links()

    def get_base_url(self):
        url = self.web_url
        slashparts = url.split('/')
        basename = '/'.join(slashparts[:3])
        return basename

    def get_link_onpage(self):
        sleep(5)
        product_raw = self.driver.find_elements_by_css_selector('div.qMZa55.JT3_zV')
        # print(f'Raw products HTML: {product_raw}')
        for product in product_raw:
            try:
                product_source_code = product.get_attribute("innerHTML")
                product_soup: BeautifulSoup = BeautifulSoup(product_source_code, 'html.parser')
                # print(product_soup.prettify())
                a_tag = product_soup.find('a', class_='_LM')
                base_url = self.get_base_url()
                source_url = f'{base_url}{a_tag.get("href")}'
                # print(f'Product source url: {source_url}')
                img_tag = a_tag.find('img')
                # print(img_tag)
                thumb_url = img_tag.get('src')
                # print(f'Thumbnail source url: {thumb_url}')
                url_details_dict_in = {'source': source_url, 'thumbnail': thumb_url,
                                       "crawling_source_url": self.web_url, 'gender': self.gender,
                                       'category': self.category, 'subcategory': self.subcategory}
                print(f"This append ==>{url_details_dict_in}")
                self.pro_links_list.append(url_details_dict_in)
            except Exception as error:
                print(f"Error in extracting source and thumb ==> {error}")

        print(f"Length Before ==> {len(self.pro_links_list)}")
        rd_pro_links_list_details = [dict(t) for t in {tuple(d.items()) for d in self.pro_links_list}]
        print(f"Length After ==> {len(rd_pro_links_list_details)}")
        os.makedirs(get_full_path("../data/jsons/"), exist_ok=True)
        with open(get_full_path("../data/jsons/subcat_links.json"), 'w') as filehandle:
            json.dump(rd_pro_links_list_details, filehandle)

    def remove_popup_banner(self):
        try:
            sleep(2)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button#uc-btn-accept-banner'))).click()
            print('Accept Cookies ==>')
            self.driver.implicitly_wait(5)
            self.driver.execute_script("window.scrollTo(0, 200)")
            sleep(2)
        except Exception as e:
            print('Error in clicking popup banner BTN : ' + str(e))

    def next_page(self):
        try:
            element = self.driver.find_elements_by_css_selector('a.cat_link-8qswi')[1]
            self.driver.execute_script("arguments[0].click();", element)
            sleep(5)
            print('Next page')
            # self.get_link_onpage()
        except Exception as e:
            print(f'Error in clicking Next page Btn : ' + str(e))
        sleep(2)

    def get_page_no(self):
        try:
            sleep(5)
            raw = self.driver.find_element_by_class_name('cat_label-2W3Y8').text
            int_page = int(str(raw.split()[-1]).strip())
            print(f'Total pages ==> {int_page}')
            return int_page
        except Exception:
            print('Quitting get_page_no')

    def infinatescroll(self):
        try:
            sleep(2)
            self.driver.execute_script("window.scrollTo(0, 1700)")
            pre = 1700
            for i in range(0, 4):
                nextscr = pre + 1700
                pre = pre + 1700
                self.driver.execute_script(f"window.scrollTo({pre}, {nextscr});")
                print('Scrolling Down...')
                # Wait to load page
                sleep(1)
        except Exception as e:
            print('Error in scrolling : ' + str(e))

    def get_pro_links(self):
        try:
            print(self.web_url)
            self.driver.get(self.web_url)
            self.remove_popup_banner()
            pages = self.get_page_no()
            self.get_link_onpage()
            for i in range(1, pages):
                self.next_page()
                self.infinatescroll()
                self.get_link_onpage()
                break
            self.driver.quit()
        except Exception as error:
            print(f'Quitting form get pro link function ==> {error}')
            self.driver.quit()


def main():
    br = 1
    for record in subcat_link_list:
        pro_link_getter = ProductLinksGetter(record)
        pro_link_getter.start()
        br = br + 1
        if br > 2:
            break


if __name__ == "__main__":
    main()
