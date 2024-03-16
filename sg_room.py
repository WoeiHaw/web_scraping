from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
from read_csv import Read_csv
from save_data import Save_data
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

now = datetime.now()
TODAY_DATE = now.strftime("%d-%m-%Y")


class Sg_room():
    def __init__(self, filename):
        # self.count_driver = 0
        self.filename = filename
        self.service = Service()
        self.options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.implicitly_wait(2)
        locations_text = []
        for i in range(15):
            try:
                locations_text = self.get_main_page(driver)
                # self.count_driver += 1
                break
            except NoSuchWindowException:
                driver.quit()
                driver = webdriver.Chrome(service=self.service, options=self.options)

            except Exception as error:
                print(f"Error in get_main_page\n{error}")

        # for num_location in range(len(locations_text) - 1):
        no_error = False
        links_for_house = []
        data_save_dict = {}
        num_locations = [i for i in range(len(locations_text))]

        for num_location in num_locations:
            rental = []
            agent_fee = []
            room_type = []
            live_in_owner = []
            aircon = []
            property_type = []
            location = []
            address = []
            wifi = []
            description = []
            links_list = []

            # if self.count_driver > 10:
            #     self.count_driver = 0
            #     driver.quit()
            #     driver = webdriver.Chrome(service=self.service, options=self.options)

            for i in range(10):
                try:
                    links_for_house = self.get_location_page(num_location, driver)
                    # self.count_driver += 1
                    break

                except (NoSuchWindowException, WebDriverException):
                    driver.quit()
                    driver = webdriver.Chrome(service=self.service, options=self.options)
                    driver.implicitly_wait(2)

                except Exception as error:

                    print(f"Error in get_location_page\n{error}")

            print(locations_text[num_location])
            print(len(links_for_house))

            for link in links_for_house:

                for i in range(10):
                    try:
                        data_dict = self.get_home_data(link, driver)
                        rental.append(data_dict["rental"])
                        agent_fee.append(data_dict["agent_fee"])
                        room_type.append(data_dict["room_type"])
                        live_in_owner.append(data_dict["live_in_owner"])
                        aircon.append(data_dict["aircon"])
                        property_type.append(data_dict["property_type"])
                        location.append(data_dict["location"])
                        address.append(data_dict["address"])
                        wifi.append(data_dict["wifi"])
                        description.append(data_dict["description"])
                        links_list.append(data_dict["link"])
                        # self.count_driver += 1
                        break

                    except (NoSuchWindowException, WebDriverException):
                        driver.quit()
                        driver = webdriver.Chrome(service=self.service, options=self.options)
                        driver.implicitly_wait(5)

                    except Exception as error:
                        print(f"Error in get_house\n{error}")

            rental = [item.replace("S$", "").replace(",", "") for item in rental]
            agent_fee = [item.replace("S$", "").replace(",", "") for item in agent_fee]
            data_save_dict["Date"] = TODAY_DATE
            data_save_dict["Rental(SGD)"] = rental
            data_save_dict["Date"] = TODAY_DATE
            data_save_dict["Agent Fee(SGD)"] = agent_fee
            data_save_dict["Room Type"] = room_type
            data_save_dict["Live_in Owner"] = live_in_owner
            data_save_dict["Aircon"] = aircon
            data_save_dict["Property Type"] = property_type
            data_save_dict["Location"] = location
            data_save_dict["Address"] = address
            data_save_dict["Description"] = description
            data_save_dict["link"] = links_list
            if len(data_save_dict["link"]) != 0:
                Save_data(self.filename, data_save_dict, True)

        driver.quit()

    def get_main_page(self, driver):
        # driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.set_page_load_timeout(10)
        driver.get("https://www.ilivesg.com/")
        search_bar = driver.find_element(By.XPATH, "//button[@type='button']")
        search_bar.click()
        locations = driver.find_elements(By.XPATH, "//ul/li/label")
        locations_text = [location.text for location in locations if location.text != '']

        return locations_text

    def get_location_page(self, num_location, driver):
        links_list_current = Read_csv(self.filename).get_links()

        # driver = webdriver.Chrome(service=self.service, options=self.options)

        driver.get("https://www.ilivesg.com/")

        search_bar = driver.find_element(By.XPATH, "//button[@type='button']")
        search_bar.click()
        locations_1 = driver.find_elements(By.XPATH, "//ul/li/label")
        locations_1 = [location for location in locations_1]

        locations_1[num_location].click()

        search_button = driver.find_element(By.XPATH, '//input[@value="Search Now"]')
        search_button.click()
        location_url = driver.current_url
        rooms = driver.find_elements(By.CLASS_NAME, 'views-row')
        rooms = [room for room in rooms]
        anchor_tag = driver.find_elements(By.XPATH, './/a[contains(., "Details")]')

        # to check whether the data is already in dataset
        links_for_house = [tag.get_attribute("href") for tag in anchor_tag if
                           tag.get_attribute("href") not in links_list_current]

        return links_for_house

    def get_home_data(self, link, driver):
        data_dict = {}
        # driver = webdriver.Chrome(service=self.service, options=self.options)
        # driver.set_page_load_timeout(5)
        driver.get(link)

        data_dict["rental"] = driver.find_element(By.XPATH, '//li[contains(., "Monthly Rent")]/div').text
        data_dict["agent_fee"] = driver.find_element(By.XPATH, '//li[contains(., "Agent Fee")]/div').text
        data_dict["room_type"] = driver.find_element(By.XPATH, '//li[contains(., "Room Type")]/div').text
        data_dict["live_in_owner"] = driver.find_element(By.XPATH, '//li[contains(., "Live-in Owner")]/div').text
        data_dict["aircon"] = driver.find_element(By.XPATH, '//li[contains(., "Aircon")]/div').text
        data_dict["property_type"] = driver.find_element(By.XPATH, '//li[contains(., "Property Type")]/div').text
        data_dict["location"] = driver.find_element(By.XPATH, '//li[contains(., "Location")]/div').text
        data_dict["address"] = driver.find_element(By.XPATH, '//li[contains(., "Address")]/div').text
        data_dict["wifi"] = driver.find_element(By.XPATH, '//li[contains(., "WIFI")]/div').text

        try:
            data_dict["description"] = driver.find_element(By.CLASS_NAME, 'mtextarea').text
        except:
            data_dict["description"] = ""
        data_dict["link"] = link

        return data_dict