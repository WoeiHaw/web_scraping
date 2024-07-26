from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from check_data import Check_data
from datetime import datetime
from save_data import Save_data
import time
import os
import requests
import re

now = datetime.now()
today_date = now.strftime("%d-%m-%Y")


class Shoes():
    def __init__(self, place, filename):
        self.service = Service()
        self.options = webdriver.ChromeOptions()
        check = Check_data(filename)
        if check.is_today_empty:
            # data_save_dict = self.get_shoes(place)
            # Save_data(filename, data_save_dict, check.is_today_empty)
            url = f"https://www.skechers.com.{place}/collections/men-shoes"
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(url)

            page_elements = driver.find_elements(By.CSS_SELECTOR, ".tt-pagination >ul>li")
            last_page = int(page_elements[-1].text)


            shoes_data = {
                "Date": [],
                "Description": [],
                "Price": [],
                "Link": []
            }
            for i in range(1, last_page + 1):
                driver.get(f"{url}?page={i}")
                new_data = self.get_shoes(driver,place)
                shoes_data["Date"] = shoes_data["Date"] + new_data["Date"]
                shoes_data["Description"] = shoes_data["Description"] + new_data["Description"]
                shoes_data["Price"] = shoes_data["Price"] + new_data["Price"]
                shoes_data["Link"] = shoes_data["Link"] + new_data["Link"]
            # shoes_data = self.get_sg_shoes(driver)

            driver.quit()
            Save_data(filename, shoes_data, check.is_today_empty,shoes_data=True)

    def get_shoes(self, driver,place):
        now = datetime.now()
        today_date = now.strftime("%d-%m-%Y")

        if place == "sg":
            path = "./assets/shoes images sg"
        elif place == "my":
            path = "./assets/shoes images my"

        description_list = []
        price_list = []
        link_list = []
        shoes = driver.find_elements(By.XPATH, '//div[@class="col-6 col-md-3 tt-col-item"]')
        links = [
            f"https://www.skechers.com.{place}{shoe.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-value')}" for
            shoe in shoes]

        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

        for link in links:

            driver.get(link)
            time.sleep(2)
            driver.get(link)
            # description = driver.find_element(By.TAG_NAME, "h1").text

            description = link[link.find("products/") + 9:].replace("-", " ").title().strip()
            description = description.replace("Gorun", "GOrun")


            match = re.search("\d{4,}", description)
            description = description[:match.start()].strip()


            # to add decimal for example  7 0 become 7.0
            match_decimal = re.search("\d \d", description)
            if match_decimal:
                description = description[:match_decimal.start() + 1] + "." + description[match_decimal.start() + 2:]
            try:
                color_container = driver.find_element(By.CSS_SELECTOR, "ul.tt-options-swatch.options-large")
                color_elements = color_container.find_elements(By.CSS_SELECTOR, "a.options-color")
                image_link = [element.get_attribute("style") for element in color_elements]

                for i in range(len(color_elements)):

                    if len(color_elements) == 1:
                        match_color = re.search(r'\d{4,}', description)
                        if match_color:
                            description = description[:match_color.end()]

                    color_elements[i].click()
                    price_tt = driver.find_elements(By.CSS_SELECTOR, ".tt-price > span")

                    price = price_tt[0].text.replace("$", "").replace("RM","").strip()

                    sku = driver.find_element(By.CSS_SELECTOR, "span.sku-js").text

                    sku_description = sku.replace("SKU:", "").strip()
                    size = re.search("-\d{1,2}", sku_description)

                    sku_description = sku_description[:size.start()]
                    description_sku = description + " - " + sku_description
                    description_sku = description_sku.replace("Slip Ins", "Slip-Ins").replace("Men Go Consistent On The Go",
                                                                                              "Men On-The-GO GO Consistent").replace(
                        "Gowalk", "GOwalk").replace("Usa", "USA").replace("Bobs", "BOBS").replace("Go Pickleball",
                                                                                                  "GO Pickleball").replace(
                        "Dc Collection", "DC Collection").replace("Arch FIt", "Arch Fit").replace("Dc Justice",
                                                                                                  "DC Justice").replace(
                        "On The Go Go", "On-The-GO GO").replace("Skech Air", "Skech-Air").replace("Skech Lite",
                                                                                                  "Skech-Lite").replace(
                        "Dlites", "D'Lites").replace("Dlux", "D'Lux").replace("On The Go", "On-The-GO").replace("Dc Comics","DC Comics").replace("Tres Air","Tres-Air")
                    description_lower = description_sku.lower()
                    index_skechers = description_lower.find("skechers", 10)
                    if index_skechers != -1:
                        description_sku = description_sku[:index_skechers] + "SKECHERS" + description_sku[
                                                                                          index_skechers + len("skechers"):]

                    description_list.append(description_sku)
                    price_list.append(price)
                    link_list.append(link)

                    if not os.path.isfile(f"{path}/{description_sku}.jpg"):
                        url = re.findall(url_regex, image_link[i])[0][0].replace("100x", "332x")
                        response = requests.get(f"https://{url}")
                        with open(f'{path}/{description_sku}.jpg', 'wb') as file:
                            file.write(response.content)

                    color_container = driver.find_element(By.CSS_SELECTOR, "ul.tt-options-swatch.options-large")
                    color_elements = color_container.find_elements(By.CSS_SELECTOR, "a.options-color")
            except NoSuchElementException:
                pass


        date = [today_date] * len(description_list)
        data_dict = {
            "Date": date,
            "Description": description_list,
            f"Price": price_list,
            "Link": link_list
        }
        return data_dict
