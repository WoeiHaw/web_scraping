from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
import time
from datetime import datetime
from check_data import Check_data
from save_data import Save_data

now = datetime.now()
TODAY_DATE = now.strftime("%d-%m-%Y")


class Facewash():
    def __init__(self):
        check = Check_data("../../Nivea Man.csv")

        self.service = Service()
        self.options = webdriver.ChromeOptions()

        if check.is_today_empty:
            self.lazada_title, self.lazada_price = self.lazada()
            self.aeon_title, self.aeon_price = self.aeon()
            self.watson_title, self.watson_price = self.watson()

            self.data_save_dict = {
                "Date": [TODAY_DATE],
                "Guardian Title": [self.lazada_title],
                "Guardian Price": [self.lazada_price],
                "Aeon Title": [self.aeon_title],
                "Aeon Price": [self.aeon_price],
                "Watson Title": [self.watson_title],
                "Watson Price": [self.watson_price]}
            Save_data("../../Nivea Man.csv", self.data_save_dict, check.is_today_empty)

        elif len(check.nan_column) != 0:

            if ("Guardian Title" in check.nan_column) | ("Guardian Price" in check.nan_column):
                self.lazada_title, self.lazada_price = self.lazada()
                self.data_save_dict = {"Guardian Title":[self.lazada_title],
                                       "Guardian Price":[self.lazada_price]}
                # self.data_save_dict["Guardian Title"].append(self.lazada_title)
                # self.data_save_dict["Guardian Price"].append(self.lazada_price)

            if ("Aeon Title" in check.nan_column) | ("Aeon Price" in check.nan_column):
                self.aeon_title, self.aeon_price = self.aeon()
                self.data_save_dict = {"Aeon Title": [self.aeon_title],
                                       "Aeon Price": [self.aeon_price]}
                # self.data_save_dict["Aeon Title"].append(self.aeon_title)
                # self.data_save_dict["Aeon Price"].append(self.aeon_price)

            if ("Watson Title" in check.nan_column) | ("Watson Price" in check.nan_column):
                self.watson_title, self.watson_price = self.watson()
                self.data_save_dict = {"Watson Title": [self.watson_title],
                                       "Watson Price": [self.watson_price]}
                # self.data_save_dict["Watson Title"].append(self.watson_title)
                # self.data_save_dict["Watson Price"].append(self.watson_price)

            Save_data("../../Nivea Man.csv", self.data_save_dict, check.is_today_empty)

    def lazada(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(
                'https://www.lazada.com.my/products/nivea-men-deep-white-oil-clear-detox-mud-foam-100g-i1299546099-s3963046423.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Anivea%252Bfor%252Bmen%252Bdeep%252Bwhite%252Boil%252Bclear%252Bmud%252Bfoam%253Bnid%253A1299546099%253Bsrc%253ALazadaMainSrp%253Brn%253A69c37cad2ac3683f149f1107f407af14%253Bregion%253Amy%253Bsku%253A1299546099_MY%253Bprice%253A17.9%253Bclient%253Adesktop%253Bsupplier_id%253A1000035173%253Bpromotion_biz%253A%253Basc_category_id%253A8080%253Bitem_id%253A1299546099%253Bsku_id%253A3963046423%253Bshop_id%253A237695&fastshipping=0&freeshipping=1&fs_ab=2&fuse_fs=&lang=en&location=Perak&price=17.9&priceCompare=&ratingscore=5.0&request_id=69c37cad2ac3683f149f1107f407af14&review=2&sale=10&search=1&source=search&spm=a2o4k.searchlist.list.i40.42414f10s5eiLK&stock=1')
            guardian_price = driver.find_element(By.CSS_SELECTOR, 'span.pdp-price_size_xl').text
            guardian_price = guardian_price.replace("RM", "")
            guardian_title = driver.find_element(By.TAG_NAME, 'h1').text
            driver.quit()
            return guardian_title, guardian_price
        except Exception as error:
            print(f"Lazada(Facewash) error:\n{error}")
            return "", ""

    def aeon(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get("https://myaeon2go.com/product/6377/men-deep-brightening-oil-clear-mud-foam")
            time.sleep(5)
            postal_code = driver.find_element(By.NAME, "postalCode")
            # print(postal_code.tag_name)
            postal_code.send_keys("81500")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="location-form"]/form/div[4]/button'))).click()
            time.sleep(5)
            aeon_price = driver.find_element(By.XPATH, '//div[@data-qa="pdp-details-price"]').text
            aeon_title = driver.find_element(By.XPATH, '//section[@data-qa="pdp-name"]').text
            driver.quit()
            aeon_price = aeon_price.replace("RM", "").strip()
            aeon_title = aeon_title.replace("\n", " ")

            return aeon_title, aeon_price
        except Exception as error:
            print(f"Aeon(Facewash) error:\n{error}")
            return "", ""

    def watson(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get("https://www.watsons.com.my/deep-white-oil-clear-mud-foam-twin-pack-2x100g/p/BP_23434")
            time.sleep(5)
            watson_title_1 = driver.find_element(By.CSS_SELECTOR, "h2.product-brand").text
            watson_title_2 = driver.find_element(By.CSS_SELECTOR, 'div.product-name').text
            watson_price = driver.find_element(By.CSS_SELECTOR, 'span.price').text

            watson_title = watson_title_1 + " " + watson_title_2
            watson_price = watson_price.replace("RM", "")
            driver.quit()
            return watson_title, watson_price
        except Exception as error:
            print(f"Watson(Facewash) error:\n{error}")
            return "", ""
