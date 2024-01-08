from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from check_data import Check_data
from datetime import datetime
from save_data import Save_data
import os
import requests

now = datetime.now()
today_date = now.strftime("%d-%m-%Y")


class Shoes():
    def __init__(self, place, filename):
        self.service = Service()
        self.options = webdriver.ChromeOptions()
        check = Check_data(filename)
        if check.is_today_empty:
            data_save_dict = self.get_shoes(place)
            Save_data(filename, data_save_dict, check.is_today_empty)

    def get_shoes(self, place):
        if place == "my":
            currency = "RM"
            path = "./assets/shoes images my"
        elif place == "sg":
            currency = "SGD $"
            path = "./assets/shoes images sg"
        for i in range(10):
            try:
                driver = webdriver.Chrome(service=self.service, options=self.options)

                driver.get(f"https://www.skechers.com.{place}/collections/men")
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

                shoes = driver.find_elements(By.XPATH, '//div[@class="col-6 col-md-3 tt-col-item"]')

                product_discription = []
                links_list = []
                price_list = []
                for shoe in shoes:
                    link = shoe.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-value')

                    prices = shoe.find_element(By.CSS_SELECTOR, "div.tt-price")

                    description = shoe.find_element(By.TAG_NAME, "h2").text

                    if description.find("-") == -1:
                        description = link[link.find("/skechers") + 1:].replace("-", " ").title().strip()
                        description = description.replace("Gorun", "GOrun")

                    addr = f"https://www.skechers.com.{place}{link}"

                    if addr != f"https://www.skechers.com.{place}/collections/men#":
                        links_list.append(addr)
                    else:
                        links_list.append("-")

                    price = prices.find_elements(By.TAG_NAME, "span")
                    price_list.append(price[0].text)
                    price_list = [price.replace("RM", "") for price in price_list]
                    product_discription.append(description)

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

                driver.quit()
                break
            except Exception as error:
                print(f"Error in get shoes\n{error}")
        date = [today_date] * len(product_discription)
        data_dict = {
            "Date": date,
            "Description": product_discription,
            f"Price ({currency})": price_list,
            "Link": links_list
        }

        return data_dict
