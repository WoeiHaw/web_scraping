from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import numpy as np
from read_csv import Read_csv
from save_data import Save_data
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from process_job_data import ProcessData
now = datetime.now()
TODAY_DATE = now.strftime("%d-%m-%Y")


class Job_info():
    def __init__(self, filename, country):
        self.service = Service()
        self.options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=self.service, options=self.options)

        for page in range(1, 32):

            # if page % 10 == 0:
            #     driver.quit()
            #     driver = webdriver.Chrome(service=self.service, options=self.options)

            jobid_list = Read_csv(filename).get_jobid()
            checked_link_list = []
            job_info_dict = {}
            # if error try 10 times
            for i in range(10):
                try:
                    checked_link_list = self.sg_job_page(page, jobid_list, country, driver)
                    break

                except (NoSuchWindowException, WebDriverException):
                    driver.quit()
                    driver = webdriver.Chrome(service=self.service, options=self.options)

                except Exception as error:
                    print(f"Error in get_house\n{error}")

            for i in range(10):
                try:
                    job_info_dict = self.get_job_info(checked_link_list, driver)
                    break

                except (NoSuchWindowException, WebDriverException):
                    driver.quit()
                    driver = webdriver.Chrome(service=self.service, options=self.options)

                except Exception as error:
                    print(f"Error in get_house\n{error}")

            if len(job_info_dict) != 0:
                Save_data(filename, job_info_dict, True)


        driver.quit()
        country_name = "Singapore" if country == "sg" else "Malaysia"
        index = filename.find(country_name)
        path = filename[:index]

        print(path)
        ProcessData(path, country_name).process_data()

    def sg_job_page(self, page, jobid_list, country, driver):

        # driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.get(f"https://www.jobstreet.com.{country}/data-science-jobs?page={page}")
        time.sleep(4)
        links = driver.find_elements(By.CSS_SELECTOR, '[data-automation="job-list-view-job-link"]')
        links_list = [link.get_attribute('href') for link in links]
        checked_link_list = []

        for link in links_list:
            try:
                index = link.find("job/")
                index2 = link.find("?", index)
                job_id = link[index + 4:index2]
            except Exception as error:
                print(error)

            if (job_id not in jobid_list) | (len(jobid_list) == 0):
                checked_link_list.append(link)

        print(f"Page：{page}")
        print(f"No of item :{len(checked_link_list)}")

        return checked_link_list

    def get_job_info(self, checked_link_list, driver):
        data_dict = {}
        job_title_list = []
        country_location_list = []
        job_description_list = []
        company_name_list = []
        posted_date_list = []
        # career_level_list = []
        # qualification_list = []
        # experience_list = []
        job_type_list = []
        job_specialization_list = []
        saved_link = []
        salary_list = []
        job_id_list = []

        for link in checked_link_list:
            for i in range(10):
                try:
                    # driver = webdriver.Chrome(service=self.service, options=self.options)
                    driver.get(link)

                    time.sleep(4)

                    job_title_list.append(driver.find_element(By.TAG_NAME, "h1").text)

                    job_description_list.append(
                        driver.find_element(By.XPATH, '//div[@data-automation="jobAdDetails"]').text)
                    company_name_list.append(
                        driver.find_element(By.CSS_SELECTOR,'[data-automation ="advertiser-name"]').text)

                    job_details = driver.find_element(By.CSS_SELECTOR,"div.y735df0._1iz8dgs6y>div.y735df0._1akoxc50._1akoxc56")
                    job_details = job_details.find_elements(By.CSS_SELECTOR,"div")
                    country_location_list.append(job_details[0].text)

                    # if len(job_details) > 2:
                    #     salary_list.append(job_details[1].text)
                    #     posted_date_list.append(job_details[2].text)
                    # elif len(job_details) == 2:
                    #     salary_list.append(' ')
                    #     posted_date_list.append(job_details[1].text)
                    # else:
                    #     salary_list.append(' ')
                    #     posted_date_list.append(' ')

                    # career_level = driver.find_elements(By.XPATH,
                    #                                     "//div[@class = 'z1s6m00 _1hbhsw6r pmwfa50 pmwfa57' and contains(., 'Career Level')]/div/div/div")

                    # qualification = driver.find_elements(By.XPATH,
                    #                                      "//div[@class = 'z1s6m00 _1hbhsw6r pmwfa50 pmwfa57' and contains(., 'Qualification')]/div/div/div")
                    # experience = driver.find_elements(By.XPATH,
                    #                                   "//div[@class = 'z1s6m00 _1hbhsw6r pmwfa50 pmwfa57' and contains(., 'Years of Experience')]/div/div/div")
                    job_type = job_details[2].text
                    job_specialization = job_details[1].text
                    posted_date_list.append(driver.find_element(By.CSS_SELECTOR,"div.y735df0._1iz8dgs6y >span.y735df0._1iz8dgs4y._94v4w0._94v4w1._94v4w22._1wzghjf4._94v4wa").text)

                    # detail = [
                        #career_level, qualification, experience,
                        # job_type, job_specialization]
                    if len(job_details) == 5:
                        salary_list.append(job_details[4].text)
                    else:
                        salary_list.append(' ')
                    # detail_list = [
                                    # career_level_list, qualification_list, experience_list,
                    job_type_list.append(job_type)
                    job_specialization_list.append(job_specialization)

                    # for i in range(len(detail)):
                    #     if len(detail[i]) == 0:
                    #         detail_list[i].append(" ")
                    #     else:
                    #         detail_list[i].append(detail[i][1].text)
                    saved_link.append(link)
                    # index1_jobid = link.find("jobId")
                    # index2_jobid = link.find("sectionRank", index1_jobid)
                    # job_id_list.append(link[index1_jobid:index2_jobid - 1])
                    index = link.find("job/")
                    index2 = link.find("?", index)
                    job_id_list.append(link[index + 4:index2])

                    break
                except Exception as error:
                    print(f"Error in getting job info\n{error}")

            today_date_list = [TODAY_DATE] * len(posted_date_list)
            data_dict = {"Date": today_date_list, "Posted Date": posted_date_list, "Title": job_title_list,
                         "Company Name": company_name_list, "Salary": salary_list,
                         "Country/Location": country_location_list,
                         "Career Level": [""]*len(posted_date_list),
                         "Qualification Requirement": [""]*len(posted_date_list),
                         "Experience Requirement": [""]*len(posted_date_list),
                         "Job Type": job_type_list, "Job Specializations": job_specialization_list,
                         "Job Description": job_description_list, "Link": saved_link, "Job ID": job_id_list}
        return data_dict
