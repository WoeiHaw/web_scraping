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
    house_item = driver.find_elements(By.XPATH, "//*[starts-with(@data-testid,'listing-ad-item-')]")

    house_link_tags = [item.find_element(By.TAG_NAME, "a") for item in house_item]

    links = [link.get_attribute('href') for link in house_link_tags if link.get_attribute('href') not in
             link_list]

    # houses = [house.text for house in houses_se]

    print(f"Page : {page}")
    print(len(links))
    return links


def get_house_info(link, driver):
    # data_dict = {}
    # property_titles = []
    # proprety_price = []
    # property_type_list = []
    # num_bedroom = []
    # num_bathroom = []
    # size_list = []
    # address_list = []
    # link_list = []
    # driver = webdriver.Chrome(service=service, options=options)

    driver.get(link)
    wait = WebDriverWait(driver, 10)  # Maximum wait time in seconds
    element = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//li[contains(.,"Property Details")]')))
    element.click()
    #     house_item = driver.find_element(By.TAG_NAME,"tbody")
    #     table_class = house_item.get_attribute('class')
    #     house_detail = driver.find_elements(By.CSS_SELECTOR, f".{table_class} tr td div div")

    time.sleep(5)
    title = driver.find_element(By.XPATH, '//h1[@itemprop="name"]').text
    house_value = driver.find_element(By.XPATH, '//div[@itemprop="offers"]').text
    property_type = driver.find_elements(By.XPATH, "//tr[contains(., 'Property Type')]/td/div")
    size = driver.find_elements(By.XPATH, "//tr[contains(., 'Size')]/td/div")
    if len(size) == 0:
        size = driver.find_elements(By.XPATH, "//tr[contains(., 'Property Size')]/td/div")
    bedrooms = driver.find_elements(By.XPATH, "//tr[contains(., 'Bedrooms')]/td/div")
    bedroom = driver.find_elements(By.XPATH, "//tr[contains(., 'Bedroom')]/td/div")
    address = driver.find_elements(By.XPATH, "//tr[contains(., 'Address')]/td/div")
    bathroom = driver.find_elements(By.XPATH, "//tr[contains(., 'Bathroom')]/td/div")

    data_list = [property_type, size, address, bathroom]

    if len(bedroom) > 0:

        bedroom_final = bedroom[0].text
    elif len(bedrooms) > 0:
        bedroom_final = bedrooms[0].text
    else:
        bedroom_final = ""

    for number in range(len(data_list)):

        if len(data_list[number]) > 0:
            data_list[number][0] = data_list[number][len(data_list[number]) - 1].text
        else:
            data_list[number] = " "

    # link_list.append(link)
    # property_titles.append(title)
    # proprety_price.append(house_value)
    # property_type_list.append(data_list[0][0])
    # size_list.append(data_list[1][0])
    # address_list.append(data_list[2][0])
    # num_bathroom.append(data_list[3][0])
    # num_bedroom.append(bedroom_final)
    # proprety_price = [price.replace("RM", "").replace(" ", "") for price in proprety_price]
    # size_list = [size.replace("sq.ft.", "").strip() for size in size_list]
    #
    # date = [TODAY_DATE] * len(link_list)

    house_value = house_value.replace("RM", "").replace(" ", "")
    data_dict = {
        "Date": TODAY_DATE,
        "Title": title,
        "Address": data_list[2][0],
        "Type": data_list[0][0],
        "Size (sq.ft)": data_list[1][0].replace("sq.ft.", ""),
        "Number of bathroom": data_list[3][0],
        "Number of bedroom": bedroom_final,
        "link": link,
        "Price": house_value
    }

    return data_dict


class House_price():
    def __init__(self, filename, place):
        self.service = Service()
        self.options = webdriver.ChromeOptions()

        driver = webdriver.Chrome(service=self.service, options=self.options)

        for page in range(1,52):
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
            # if page % 10 == 0 :
            #     driver.quit()
            #     driver = webdriver.Chrome(service=self.service, options=self.options)

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
                        print(f"Error in get_house\n{error}")

            if len(data_to_save["Title"]) != 0:
                Save_data(filename, data_to_save, True)

        driver.quit()
        ProcessHousePrice(filename[:filename.find("House")], "JB" if place == "johor+bahru" else "kl").process()
