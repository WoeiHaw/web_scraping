from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from check_data import Check_data
from save_data import Save_data
import os

now = datetime.now()
TODAY_DATE = now.strftime("%d-%m-%Y")


class Coffee:
    def __init__(self, filename):

        # super()._init_()

        self.filename = filename
        self.service = Service()
        self.options = webdriver.ChromeOptions()
        check = Check_data(self.filename)
        if check.is_today_empty:
            self.shopee_title, self.shopee_price = self.scrape_coffe_shopee()
            self.lazada_title, self.lazada_price = self.scrape_coffe_lazada()
            self.pg_title, self.pg_price = self.scrape_coffe_pgmall()

            self.data_save_dict = {
                "Date": [TODAY_DATE],
                "Title Shopee": [self.shopee_title],
                "Shopee Price": [self.shopee_price],
                "Title Lazada": [self.lazada_title],
                "Lazada Price": [self.lazada_price],
                "Title PGMall": [self.pg_title],
                "PGMall Price": [self.pg_price]}
            Save_data(self.filename, self.data_save_dict, check.is_today_empty)

        elif len(check.nan_column) != 0:

            if ("Title Shopee" in check.nan_column) | ("Shopee Price" in check.nan_column):
                self.shopee_title, self.shopee_price = self.scrape_coffe_shopee()
                self.data_save_dict = {"Title Shopee": [self.shopee_title],
                                       "Shopee Price": [self.shopee_price]}
                Save_data(self.filename, self.data_save_dict, check.is_today_empty)

            if ("Title Lazada" in check.nan_column) | ("Lazada Price" in check.nan_column):
                self.lazada_title, self.lazada_price = self.scrape_coffe_lazada()
                self.data_save_dict = {"Title Lazada": [self.lazada_title],
                                       "Lazada Price": [self.lazada_price]}
                Save_data(self.filename, self.data_save_dict, check.is_today_empty)

            if ("Title PGMall" in check.nan_column) | ("PGMall Price" in check.nan_column):
                self.pg_title, self.pg_price = self.scrape_coffe_pgmall()
                self.data_save_dict = {"Title PGMall": [self.pg_title],
                                       "PGMall Price": [self.pg_price]}
                Save_data(self.filename, self.data_save_dict, check.is_today_empty)

            # Save_data(self.filename, self.data_save_dict, check.is_today_empty)

    def scrape_coffe_shopee(self):

        # Shopee
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(
                "https://shopee.com.my/Kluang-Coffee-Cap-Televisyen-Kopi-O-Kosong-Eco-Pack-(100-sachets-x-1-Pack)-Kopi-O-Kluang-Cap-TV-i.25563366.498280783?sp_atk=72da7cb5-8cca-435e-8fb7-44f1f0289c18&xptdk=72da7cb5-8cca-435e-8fb7-44f1f0289c18")
            driver.refresh()
            time.sleep(5)
            # WebDriverWait(driver, 20).until(
            #     EC.element_to_be_clickable(
            #         (By.XPATH, '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button'))).click()

            email_tab = driver.find_element(By.NAME, "loginKey")
            password_tab = driver.find_element(By.NAME, "password")
            time.sleep(5)
            email_tab.send_keys("")
            password_tab.send_keys("")

            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Log In')]")))
            button = driver.find_element(By.XPATH,
                                         "//button[contains(text(),'Log In')]")

            button.click()
            time.sleep(5)
            title_shopee = driver.find_element(By.XPATH,
                                               '//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/div[1]/span').text
            price_shopee = driver.find_element(By.CSS_SELECTOR, 'div.pqTWkA').text

            price_shopee = price_shopee.replace("RM", "").strip()

            driver.quit()
            return title_shopee, price_shopee
        except Exception as error:
            message = f"An exception occur in Shopee(coffee): \n{error}"
            print(message)
            return "", ""

    def scrape_coffe_lazada(self):
        try:
            url = "https://www.lazada.com.my/products/kluang-kopi-o-kosong-cap-televisyen-black-coffee-eco-pack-100-sachets-x-10gm-kopi-o-kluang-cap-tv-i143287346-s165887570.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Akluang%252Bcoffee%252Bcap%252Btelevision%253Bnid%253A143287346%253Bsrc%253ALazadaMainSrp%253Brn%253A3bb9bca68b7e207e3442369df68c77cf%253Bregion%253Amy%253Bsku%253AKL102WNAB7XV4KANMY%253Bprice%253A26.99%253Bclient%253Adesktop%253Bsupplier_id%253A37100%253Bpromotion_biz%253A%253Basc_category_id%253A10003110%253Bitem_id%253A143287346%253Bsku_id%253A165887570%253Bshop_id%253A1193&fastshipping=0&freeshipping=1&fs_ab=2&fuse_fs=1&lang=en&location=Johor&price=26.99&priceCompare=&ratingscore=4.939313984168866&request_id=3bb9bca68b7e207e3442369df68c77cf&review=1137&sale=4316&search=1&source=search&spm=a2o4k.searchlist.list.i40.4e906efbkIyue3&stock=1"
            driver = webdriver.Chrome(service=self.service, options=self.options)

            driver.get(url)
            time.sleep(5)
            title_lazada = driver.find_element(By.CSS_SELECTOR, "h1.pdp-mod-product-badge-title").text
            price_lazada = driver.find_element(By.CSS_SELECTOR, "div.pdp-product-price > span.pdp-price").text
            price_lazada = price_lazada.replace("RM", "").strip()
            time.sleep(5)
            driver.quit()
            return title_lazada, price_lazada
        except Exception as error:
            message = f"An exception occur in Lazada(coffee): \n{error}"
            print(message)
            return "", ""

    def scrape_coffe_pgmall(self):
        try:
            url = "https://pgmall.my/p/WH42/7744"
            driver = webdriver.Chrome(service=self.service, options=self.options)

            driver.get(url)
            time.sleep(5)
            title_pg = driver.find_element(By.ID, "prod_name").text
            price_pg = driver.find_element(By.CSS_SELECTOR, "div.price-col").text

            price_pg = price_pg.split("/")[0].replace("RM", "").strip()

            driver.quit()
            return title_pg, price_pg
        except Exception as error:
            message = f"An exception occur in Pg Mall(coffee): \n{error}"
            print(message)
            return "", ""