import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from check_data import Check_data
from datetime import datetime
from save_data import Save_data

now = datetime.now()
today_date = now.strftime("%d-%m-%Y")


class Shoes():
    def __init__(self,place,filename):
        self.service = Service()
        self.options = webdriver.ChromeOptions()
        check = Check_data(filename)
        if check.is_today_empty:
            data_save_dict = self.get_shoes(place)
            Save_data(filename, data_save_dict, check.is_today_empty)

    def get_shoes(self, place):
        if place == "my":
            currency = "RM"
        elif place =="sg":
            currency = "SGD $"
        for i in range(10):
            try:
                driver = webdriver.Chrome(service=self.service, options=self.options)

                driver.get(f"https://www.skechers.com.{place}/collections/men-sport")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.implicitly_wait(2)
                    try:
                        if driver.find_element(By.XPATH,
                                               '//div[@class="show-more tt_item_all_js"]').text == "NO MORE PRODUCTS":
                            break
                    except:
                        pass

                shoes = driver.find_elements(By.XPATH, '//div[@class="col-6 col-md-3 tt-col-item"]')

                product_discription = []
                links_list = []
                price_list = []
                for shoe in shoes:
                    links = shoe.find_elements(By.TAG_NAME, 'a')

                    prices = shoe.find_element(By.CSS_SELECTOR, "div.tt-price")

                    description = shoe.find_element(By.TAG_NAME, "h2")
                    for link in links:
                        addr = link.get_attribute("href")
                        if addr != f"https://www.skechers.com.{place}/collections/men-sport#":
                            links_list.append(addr)
                            break
                    price = prices.find_elements(By.TAG_NAME, "span")
                    price_list.append(price[0].text)
                    price_list = [price.replace("RM", "") for price in price_list]
                    product_discription.append(description.text)

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
