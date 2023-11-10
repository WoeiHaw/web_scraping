from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
import time
from datetime import datetime
import pandas as pd
from check_data import Check_data
from save_data import Save_data

now = datetime.now()
TODAY_DATE = now.strftime("%d-%m-%Y")


class Shapoo():
    def __init__(self, filename):

        self.service = Service()
        self.options = webdriver.ChromeOptions()
        self.filename = filename
        check = Check_data(self.filename)

        if check.is_today_empty:
            self.watson_title, self.watson_price = self.watson()
            self.guardian_title, self.guardian_price = self.guardian()
            self.lotus_title, self.lotus_price = self.lotus()

            self.data_save_dict = {
                "Date": [TODAY_DATE],
                "Watson Title": [self.watson_title],
                "Watson Price": [self.watson_price],
                "Guardian Title": [self.guardian_title],
                "Guardian Price": [self.guardian_price],
                "Lotus Title": [self.lotus_title],
                "Lotus Price": [self.lotus_price]}
            Save_data(self.filename, self.data_save_dict, check.is_today_empty)

        elif len(check.nan_column) != 0:

            if ("Watson Title" in check.nan_column) | ("Watson Price" in check.nan_column):
                self.watson_title, self.watson_price = self.watson()
                self.data_save_dict = {"Watson Title": [self.watson_title],
                                       "Watson Price": [self.watson_price]}

            if ("Guardian Title" in check.nan_column) | ("Guardian Price" in check.nan_column):
                self.guardian_title, self.guardian_price = self.guardian()
                self.data_save_dict = {"Guardian Title": [self.guardian_title],
                                       "Guardian Price": [self.guardian_price]}

            if ("Lotus Title" in check.nan_column) | ("Lotus Price" in check.nan_column):
                self.lotus_title, self.lotus_price = self.lotus()
                self.data_save_dict = {"Lotus Title": [self.lotus_title],
                                       "Lotus Price": [self.lotus_price]}

            Save_data(self.filename, self.data_save_dict, check.is_today_empty)

    def watson(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get('https://www.watsons.com.my/ultra-men-cool-menthol-shampoo-480ml/p/BP_71638')
            time.sleep(3)
            watson_title = f"{driver.find_element(By.CSS_SELECTOR, 'h2.product-brand').text} {driver.find_element(By.CSS_SELECTOR, 'div.product-name').text}"

            watson_price = driver.find_element(By.CSS_SELECTOR, "span.price").text
            driver.quit()
            return watson_title, watson_price
        except Exception as error:
            print(f"watson error(Shampoo):\n{error}")
            return "", ""

    def guardian(self):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        url = "https://guardian.com.my/hs-umen-spoo-480ml-cmenthol-121102473.html?page=1"
        driver.get(url)
        time.sleep(2)
        driver.get(url)
        time.sleep(5)
        try:
            guardian_title = driver.find_element(By.CSS_SELECTOR, "h1.productFullDetail-productName-22A").text
            guardian_price = driver.find_element(By.CSS_SELECTOR, "div.price-maxPrice2-SZb").text
            guardian_price = guardian_price.split()[1]
            driver.quit()
            return guardian_title, guardian_price
        except Exception as error:
            print(f"guardian error(Shampoo):\n{error}")
            guardian_title = ""
            guardian_price = ""
            return guardian_title, guardian_price

    def lotus(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get('https://www.lotuss.com.my/en/product/hns-shp-men-cool-menthol-480ml-73817120')
            time.sleep(5)
            lotus_title = driver.find_element(By.CSS_SELECTOR, "h1").text
            lotus_price = driver.find_element(By.XPATH,
                                              '//*[@id="spa-root"]/div/div[1]/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[1]').text
            lotus_price = lotus_price.split("/")[0].replace("RM", "")
            driver.quit()
            return lotus_title, lotus_price
        except Exception as error:
            print(f"guardian error(Shampoo):\n{error}")
            return "", ""

