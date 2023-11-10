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


class Toothpaste():
    def __init__(self, filename):

        self.service = Service()
        self.options = webdriver.ChromeOptions()
        self.filename = filename
        check = Check_data(self.filename)
        if check.is_today_empty:
            self.watson_title, self.watson_price = self.watson()
            self.guardian_title, self.guardian_price = self.guardian()
            self.big_pham_title, self.big_pham_price = self.big_pham()

            self.data_save_dict = {
                "Date": [TODAY_DATE],
                "Guardian Title": [self.guardian_title],
                "Guardian Price": [self.guardian_price],
                "BigPharmacy Title": [self.big_pham_title],
                "BigPharmacy Price": [self.big_pham_price],
                "Watson Title": [self.watson_title],
                "Watson Price": [self.watson_price]}
            Save_data(self.filename, self.data_save_dict, check.is_today_empty)

        elif len(check.nan_column) != 0:

            if ("Guardian Title" in check.nan_column) | ("Guardian Price" in check.nan_column):
                self.guardian_title, self.guardian_price = self.guardian()
                self.data_save_dict = {"Guardian Title": [self.guardian_title],
                                       "Guardian Price": [self.guardian_price]}

            if ("BigPharmacy Title" in check.nan_column) | ("BigPharmacy Price" in check.nan_column):
                self.big_pham_title, self.big_pham_price = self.big_pham()
                self.data_save_dict = {"BigPharmacy Title": [self.big_pham_title],
                                       "BigPharmacy Price": [self.big_pham_price]}

            if ("Watson Title" in check.nan_column) | ("Watson Price" in check.nan_column):
                self.watson_title, self.watson_price = self.watson()
                self.data_save_dict = {"Watson Title": [self.watson_title],
                                       "Watson Price": [self.watson_price]}

            Save_data(self.filename, self.data_save_dict, check.is_today_empty)

    def watson(self):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.get("https://www.watsons.com.my/double-action-2-x-225g./p/BP_73200")
        time.sleep(3)
        try:
            watson_title_1 = driver.find_element(By.TAG_NAME, "h2").text
            watson_title_2 = driver.find_element(By.CSS_SELECTOR, 'div.product-name').text
            watson_price = driver.find_element(By.CLASS_NAME, 'price').text
            driver.quit()
            watson_title = watson_title_1 + " " + watson_title_2
            watson_price = watson_price.replace("RM", "")
            return watson_title, watson_price
        except Exception as error:
            watson_title = ""
            watson_price = ""
            print(f"Watson(Toothpaste) error:\n{error}")
            return watson_title, watson_price

    def guardian(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            url = "https://guardian.com.my/darlie-225g-po2gwp-tp-121090556.html?utm_source=google&utm_medium=seller&utm_campaign=s547820454_SS_MY_GSHP_guardianshopping2022&is_seller=true&gclid=Cj0KCQjwqs6lBhCxARIsAG8YcDgY6m831IOCWJkCVsVIQeRCtzhz4VciXumGEcleW5xOy0F4UhdWWhkaAlD6EALw_wcB&page=1"
            driver.get(url)
            time.sleep(2)
            driver.get(url)
            time.sleep(5)
            guardian_title = driver.find_element(By.TAG_NAME, "h1").text
            guardian_price = driver.find_element(By.CSS_SELECTOR, "div.price-maxPrice-1_b").text
            driver.quit()
            index = guardian_title.find("\n")
            guardian_title = guardian_title[:index]
            guardian_price = guardian_price.replace("MYR", "").strip()
            return guardian_title, guardian_price
        except Exception as error:
            print(f"Guardian(Toothpaste) error:\n{error}")
            return "", ""

    def big_pham(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get("https://www.bigpharmacy.com.my/darlie-tpaste-double-action-225gx2-mint-flavor")
            time.sleep(4)
            big_pham_title = driver.find_element(By.CSS_SELECTOR, "td.prodDetail_name_quickview").text
            big_pham_price = driver.find_element(By.XPATH,
                                                 '//*[@id="cart_quantity"]/div[3]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]').text
            driver.quit()
            big_pham_price = big_pham_price.replace("RM", "").strip()
            return big_pham_title, big_pham_price
        except Exception as error:
            print(f"Big Pham(Toothpaste) error:\n{error}")
            return "", ""
