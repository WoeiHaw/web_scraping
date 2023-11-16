from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import requests

class Shoes_image():
    def __init__(self,place):
        service = Service()
        options = webdriver.ChromeOptions()
        if place == "my":
            path = "./assets/shoes images my"
        elif place == "sg":
            path = "./assets/shoes images sg"

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(f"https://www.skechers.com.{place}/collections/men")

        isStop = False
        count = 0
        while not isStop:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)
            isStop = False if count <= 50 else True
            try:
                if driver.find_element(By.XPATH,
                                       '//div[@class="show-more tt_item_all_js"]').text == "NO MORE PRODUCTS":
                    break
            except:
                pass
            count += 1
        shoes = driver.find_elements(By.XPATH, '//div[@class="col-6 col-md-3 tt-col-item"]')
        for shoe in shoes:
            description = shoe.find_element(By.TAG_NAME, "h2").text

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