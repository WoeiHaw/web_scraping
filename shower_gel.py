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


class Dettol():
    def __init__(self, filename):

        self.service = Service()
        self.options = webdriver.ChromeOptions()
        self.filename = filename
        check = Check_data(self.filename)
        if check.is_today_empty:
            self.watson_title, self.watson_price = self.watson()
            self.aeon_title, self.aeon_price = self.aeon()
            self.guardian_title, self.guardian_price = self.guardian()
            self.caring_title, self.caring_price = self.caring()
            try:
                guardian_price_float_pcs = float(self.guardian_price) / 2
            except:
                guardian_price_float_pcs = ""
            self.data_save_dict = {
                "Date": [TODAY_DATE],
                "Title Watson": [self.watson_title],
                "Price Watson": [self.watson_price],
                "Price/pcs (Watson)": [self.watson_price],
                "Title Aeon": [self.aeon_title],
                "Price Aeon": [self.aeon_price],
                "Price/pcs (Aeon)": [self.aeon_price],
                "Title Guardian": [self.guardian_title],
                "Price Guardian": [self.guardian_price],
                "Price/pcs (Guardian)": [guardian_price_float_pcs],
                "Title Caring": [self.caring_title],
                "Price Caring": [self.caring_price],
                "Price/pcs (Caring)": [self.caring_price]
            }
            Save_data(self.filename, self.data_save_dict, check.is_today_empty)

        elif len(check.nan_column) != 0:

            if ("Title Watson" in check.nan_column) | ("Price Watson" in check.nan_column):
                self.watson_title, self.watson_price = self.watson()
                self.data_save_dict = {"Title Watson": [self.watson_title],
                                       "Price Watson": [self.watson_price],
                                       "Price/pcs (Watson)": [self.watson_price]}

            if ("Title Aeon" in check.nan_column) | ("Price Aeon" in check.nan_column):
                self.aeon_title, self.aeon_price = self.aeon()
                self.data_save_dict = {"Title Aeon": [self.aeon_title],
                                       "Price Aeon": [self.aeon_price],
                                       "Price/pcs (Aeon)": [self.aeon_price]}
                Save_data(self.filename, self.data_save_dict, check.is_today_empty)

            if ("Title Guardian" in check.nan_column) | ("Price Guardian" in check.nan_column):
                self.guardian_title, self.guardian_price = self.guardian()
                self.data_save_dict = {"Title Guardian": [self.guardian_title],
                                       "Price Guardian": [self.guardian_price],
                                       "Price/pcs (Guardian)": [float(self.guardian_price) / 2]}
                Save_data(self.filename, self.data_save_dict, check.is_today_empty)

            if ("Title Caring" in check.nan_column) | ("Price Caring" in check.nan_column):
                self.caring_title, self.caring_price = self.caring()
                self.data_save_dict = {"Title Caring": [self.caring_title],
                                       "Price Caring": [self.caring_price],
                                       "Price/pcs (Caring)": [self.caring_price]}
                Save_data(self.filename, self.data_save_dict, check.is_today_empty)
            # Save_data(self.filename, self.data_save_dict, check.is_today_empty)

    def watson(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get("https://www.watsons.com.my/shower-gel-lasting-fresh-950g/p/BP_92249")
            time.sleep(5)
            watson_title = driver.find_element(By.CLASS_NAME, "product-name").text
            watson_price = driver.find_element(By.CSS_SELECTOR, "span.price").text
            driver.quit()
            return watson_title, watson_price
        except Exception as error:
            print(f"watson error (Shower Gel):\n{error}")
            return "", ""

    def aeon(self):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get("https://myaeon2go.com/product/5469/shower-gel-lasting-fresh")
            time.sleep(2)
            postal_code = driver.find_element(By.NAME, "postalCode")
            postal_code.send_keys("81500")

            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//section[@id="location-form"]/form/div/button'))).click()
            time.sleep(5)
            aeon_title = driver.find_element(By.CSS_SELECTOR, "section.R1_tOog0IelmdG6HHC1g").text
            aeon_price = driver.find_element(By.CSS_SELECTOR, "span.eWWWefEZnMjXklZCSPch").text
            aeon_price = float(aeon_price.replace("RM", "").strip())
            unit_aeon = driver.find_element(By.CSS_SELECTOR, "div.czXzIdRs3ZRSbzoP4pWb").text
            aeon_title = aeon_title.replace("\n", " ")
            aeon_title = aeon_title + " " + unit_aeon
            driver.quit()
            return aeon_title, aeon_price
        except Exception as error:
            print(f"Aeon error(Shower Gel):\n{error}")
            return "", ""

    def guardian(self):
        url = "https://guardian.com.my/dettol-sg-950ml-po2-lfresh-121110440.html?page=1"
        driver = driver = webdriver.Chrome(service=self.service, options=self.options)

        try:
            driver.get(url)
            time.sleep(3)
            driver.get(url)
            time.sleep(5)
            guardian_title = driver.find_element(By.CSS_SELECTOR, "h1.productFullDetail-productName-22A").text
            guardian_price = driver.find_element(By.CSS_SELECTOR, "div.price-maxPrice-1_b").text
            guardian_price = guardian_price.replace("MYR", "").strip()
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/aside[2]/form/div/div[2]/div[2]/button'))).click()
            time.sleep(5)
            driver.quit()
            return guardian_title, guardian_price
        except Exception as error:
            print(f"Gueardian error(Shower Gel):\n{error}")
            guardian_title = ""
            guardian_price = ""
            return guardian_title, guardian_price

    def caring(self):
        try:
            url = "https://estore.caring2u.com/dettol-shower-gel-lasting-fresh-950ml-g.html"
            driver = webdriver.Chrome(service=self.service, options=self.options)

            driver.get(url)
            time.sleep(5)
            caring_title = driver.find_element(By.CSS_SELECTOR, "h1.page-title").text
            caring_price = driver.find_element(By.CSS_SELECTOR, "span.price").text
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/aside[2]/form/div/div[2]/div[2]/button'))).click()
            time.sleep(5)
            driver.quit()
            caring_price = caring_price.replace("RM", "").strip()
            return caring_title, caring_price
        except Exception as error:
            print(f"Caring error(Shower Gel):\n{error}")
            return "", ""
