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
            url = f"https://www.skechers.com.{place}/collections/men"
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(url)
            if place == "my":
                page_elements = driver.find_elements(By.CSS_SELECTOR, ".tt-pagination >ul>li")
                pages = []
                last_page = int(page_elements[-1].text)
                shoes_data = {
                    "Date": [],
                    "Description": [],
                    "Price (RM)": [],
                    "Link": []
                }
                for i in range(1, last_page + 1):
                    driver.get(f"{url}?page={i}")
                    new_data = self.get_my_shoes(driver)
                    shoes_data["Date"] = shoes_data["Date"] + new_data["Date"]
                    shoes_data["Description"] = shoes_data["Description"] + new_data["Description"]
                    shoes_data["Price (RM)"] = shoes_data["Price (RM)"] + new_data["Price (RM)"]
                    shoes_data["Link"] = shoes_data["Link"] + new_data["Link"]
            elif place == "sg":
                isStop = False
                count = 0
                while not isStop:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.implicitly_wait(2)
                    isStop = False if count <= 100 else True
                    try:
                        if driver.find_element(By.XPATH,
                                               '//div[@class="show-more tt_item_all_js"]').text == "NO MORE PRODUCTS":
                            break
                    except:
                        pass
                    count += 1
                shoes_data = self.get_sg_shoes(driver)

            driver.quit()
            Save_data(filename, shoes_data, check.is_today_empty)

    def get_sg_shoes(self, driver):
        now = datetime.now()
        today_date = now.strftime("%d-%m-%Y")

        currency = "SGD $"
        path = "./assets/shoes images sg"

        shoes = driver.find_elements(By.XPATH, '//div[@class="col-6 col-md-3 tt-col-item"]')

        product_discription = []
        links_list = []
        price_list = []
        for shoe in shoes:
            link = shoe.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-value')

            prices = shoe.find_element(By.CSS_SELECTOR, "div.tt-price")
            # prices = prices.find_elements(By.TAG_NAME, "span")[0].text
            #         price_list.append(price[0].text)
            price = prices.find_elements(By.TAG_NAME, "span")
            price_list.append(price[0].text)
            price_list = [price.replace("RM", "") for price in price_list]

            description = shoe.find_element(By.TAG_NAME, "h2").text
            description = description.replace("Arch FIt","Arch Fit")
            product_discription.append(description)

            addr = f"https://www.skechers.com.sg{link}"

            if addr != f"https://www.skechers.com.sg/collections/men#":

                links_list.append(addr)
            else:
                links_list.append("-")

            if not os.path.isfile(f"{path}/{description}.jpg"):

                img = shoe.find_element(By.CSS_SELECTOR, "img.lazyload")
                img_link = img.get_attribute("data-srcset")

                try:
                    indx_start = img_link.split(',')[1].find("BBK_")
                    indx_end = img_link.split(',')[1].find(".jpg")
                    img_link_final = img_link.split(',')[1]
                    img_link_final = f"{img_link_final[:indx_start]}BBK_240x{img_link_final[indx_end:]}"
                except IndexError:
                    indx_start = img_link.split(',')[0].find("BBK_")
                    indx_end = img_link.split(',')[0].find(".jpg")
                    img_link_final = img_link.split(',')[0]
                    img_link_final = f"{img_link_final[:indx_start]}BBK_240x{img_link_final[indx_end:]}"
                #         img_link_final = img_link.split(',')[0]#.replace("332","240")
                response = requests.get(f"https:{img_link_final}")
                with open(f'{path}/{description}.jpg', 'wb') as file:
                    file.write(response.content)
        date = [today_date] * len(product_discription)
        data_dict = {
            "Date": date,
            "Description": product_discription,
            f"Price ({currency})": price_list,
            "Link": links_list
        }

        return data_dict

    def get_my_shoes(self, driver):
        now = datetime.now()
        today_date = now.strftime("%d-%m-%Y")
        currency = "RM"
        path = "./assets/shoes images my"

        description_list = []
        price_list = []
        link_list = []
        shoes = driver.find_elements(By.XPATH, '//div[@class="col-6 col-md-3 tt-col-item"]')
        links = [
            f"https://www.skechers.com.my{shoe.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-value')}" for
            shoe in shoes]

        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

        for link in links:

            driver.get(link)
            time.sleep(2)
            # description = driver.find_element(By.TAG_NAME, "h1").text
            try:
                price = driver.find_element(By.CSS_SELECTOR, ".sale-price").text.replace("RM", "").strip()
            except NoSuchElementException:
                price = driver.find_element(By.CSS_SELECTOR, ".new-price").text.replace("RM", "").strip()

            description = link[link.find("/skechers") + 1:].replace("-", " ").title().strip()
            description = description.replace("Gorun", "GOrun")

            # to add "-" before the shoes' model number
            match = re.search("\d{5,6}", description)
            description = description[:match.start() - 1] + " - " + description[match.start():]

            # to add decimal for example  7 0 become 7.0
            match_decimal = re.search("\d \d", description)
            if match_decimal:
                description = description[:match_decimal.start() + 1] + "." + description[match_decimal.start() + 2:]

            color_container = driver.find_element(By.CSS_SELECTOR, "ul.tt-options-swatch.options-large")
            color_elements = color_container.find_elements(By.CSS_SELECTOR, "a.options-color")
            image_link = [element.get_attribute("style") for element in color_elements]

            for i in range(len(color_elements)):
                description_sku = ""
                if len(color_elements) == 1:
                    match_color = re.search(r'\d{4,}',description)
                    if match_color:
                        description = description[:match_color.end()]
                color_elements[i].click()
                sku = driver.find_element(By.CSS_SELECTOR, "span.sku-js").text
                color = re.search("-\D{3,5}-", sku).group()
                # to remove the last "-" in color
                color = color[:-1]

                description_sku = description + color
                description_sku = description_sku.replace("Slip Ins","Slip-Ins").replace("Gowalk","GOwalk").replace("Usa","USA").replace("Bobs","BOBS").replace("Go Pickleball","GO Pickleball").replace("Dc Collection","DC Collection").replace("Arch FIt","Arch Fit").replace("Dc Justice","DC Justice")
                description_lower = description_sku.lower()
                index_skechers = description_lower.find("skechers", 10)
                if index_skechers != -1:
                    description_sku = description_sku[:index_skechers] + "SKECHERS" + description_sku[index_skechers + len("skechers"):]

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

        date = [today_date] * len(description_list)
        data_dict = {
            "Date": date,
            "Description": description_list,
            f"Price ({currency})": price_list,
            "Link": link_list
        }
        return data_dict
