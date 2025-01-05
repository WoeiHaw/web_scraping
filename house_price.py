from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from read_csv import Read_csv
from save_data import Save_data
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from process_house_price import ProcessHousePrice

now = datetime.now()
TODAY_DATE = now.strftime("%d-%m-%Y")
service = Service()
options = webdriver.ChromeOptions()


def get_house(page, link_list, place, driver):
    # driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"https://www.mudah.my/malaysia/properties-for-sale?o={page}&q={place}")
    time.sleep(3)
    house_item = driver.find_elements(By.CSS_SELECTOR, ".Card__CardContainer-sc-11o95rz-0.etPCUE")

    house_link_tags = [item.find_element(By.TAG_NAME, "a") for item in house_item]

    links = [link.get_attribute('href') for link in house_link_tags if link.get_attribute('href') not in
             link_list]

    print(f"Page : {page}")
    print(len(links))
    return links


def get_house_info(link, driver):
    driver.get(link)

    time.sleep(5)

    title = driver.find_elements(By.XPATH, "//div[div/h2]/p")[0].text

    house_value = (driver.find_elements(By.CSS_SELECTOR, "h2>span")[0]
                   .text.replace("RM", "").replace(",", "").strip())

    property_type = driver.find_elements(By.XPATH, "//div[p[contains(text(), 'Property Type')]]/p")[1].text

    property_info = driver.find_elements(By.CSS_SELECTOR,
                                         "div.Box-bx23rg-0.Flex-sc-9pwi7j-0.style__BottomWrapper-iwjn3z-3.dylTuM >"
                                         "div")

    if len(property_info) == 0:
        size = "0"
        bedroom = "0"
        bathroom = "0"
    elif len(property_info) == 1:
        size = property_info[0].text
        bedroom = "0"
        bathroom = "0"
    else:
        size = property_info[0].text
        bedroom = property_info[1].text.replace("Bed", "").strip()
        bathroom = property_info[2].text.replace("Bath", "").strip()

    size = size.replace("sq.ft", "").replace(",", "").strip()
    if size.find("Acre(s)") != -1:
        size = size.replace(" Acre(s)", "").strip()
        size += " Acres"

    try:
        address = driver.find_elements(By.CSS_SELECTOR,
                                       "div.Box-bx23rg-0.col-span-2.Flex-sc-9pwi7j-0.cffChp > p")[-1].text
    except Exception as err:
        address = ""

    data_dict = {
        "Date": TODAY_DATE,
        "Title": title,
        "Address": address,
        "Type": property_type,
        "Size (sq.ft)": size,
        "Number of bathroom": bathroom,
        "Number of bedroom": bedroom,
        "link": link,
        "Price": house_value
    }
    return data_dict


class House_price():
    def __init__(self, filename, place):
        self.service = Service()
        self.options = webdriver.ChromeOptions()

        driver = webdriver.Chrome(service=self.service, options=self.options)

        for page in range(1, 52):
            house_link = []
            data_to_save = {
                "Date": [],
                "Title": [],
                "Address": [],
                "Type": [],
                "Size (sq.ft)": [],
                "Number of bathroom": [],
                "Number of bedroom": [],
                "link": [],
                "Price": []
            }

            link_list = Read_csv(filename).get_links()
            for i in range(10):
                try:
                    house_link = get_house(page, link_list, place, driver)
                    break
                except (NoSuchWindowException, WebDriverException):
                    driver.quit()
                    driver = webdriver.Chrome(service=service, options=options)
                except Exception as error:
                    print(f"Error in get_house\n{error}")

            for link in house_link:

                for i in range(10):
                    try:

                        data_dict = get_house_info(link, driver)

                        data_to_save["Date"].append(data_dict["Date"])
                        data_to_save["Title"].append(data_dict["Title"])
                        data_to_save["Address"].append(data_dict["Address"])
                        data_to_save["Type"].append(data_dict["Type"])
                        data_to_save["Size (sq.ft)"].append(data_dict["Size (sq.ft)"])
                        data_to_save["Number of bathroom"].append(data_dict["Number of bathroom"])
                        data_to_save["Number of bedroom"].append(data_dict["Number of bedroom"])
                        data_to_save["link"].append(data_dict["link"])
                        data_to_save["Price"].append(data_dict["Price"])
                        break
                    except (NoSuchWindowException, WebDriverException):
                        driver.quit()
                        driver = webdriver.Chrome(service=service, options=options)
                    except Exception as error:
                        print(f"Error in get_house_info\n{error}")

            if len(data_to_save["Title"]) != 0:
                Save_data(filename, data_to_save, True)

        driver.quit()
        ProcessHousePrice(filename[:filename.find("House")], "JB" if place == "johor+bahru" else "kl").process()
