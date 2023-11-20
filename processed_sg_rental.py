import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from difflib import SequenceMatcher

class Process_data():
    def __init__(self,path):
        def similar(str1, str2):
            return SequenceMatcher(None, str1, str2).ratio()

        def drop_duplicate_row(duplicated_items, duplicated_column_name, check_item_column_name, rental):
            for i in range(len(duplicated_items)):
                isFirst = True
                isbreak = False
                while isFirst | isbreak:
                    isbreak = False
                    isFirst = False
                    item = duplicated_items[i]
                    data = rental[rental[duplicated_column_name] == item]
                    for j in range(len(data)):
                        data_series = data.iloc[j]
                        if isbreak:
                            break
                        for k in range(len(data)):
                            if j != k:

                                similar_score = similar(data.iloc[k][check_item_column_name],
                                                        data.iloc[j][check_item_column_name])

                                if (similar_score >= 0.75) & (
                                        data.iloc[j]["Rental(SGD)"] == data.iloc[k]["Rental(SGD)"]):
                                    rental.drop(index=data.iloc[k].name, inplace=True)
                                    isbreak = True
                                    break
                                else:
                                    isbreak = False

        rental_df = pd.read_csv(path + "sg rental.csv")
        rental_df["Adress_check"] = rental_df["Address"].apply(
            lambda x: x.strip().lower().replace(",", "").replace(" ", ""))
        rental_df["Description_check"] = rental_df["Description"].apply(
            lambda x: x.strip().lower().replace(",", "").replace("\n", "").replace(" ", "") if type(x) == str else "-")
        rental_df.drop_duplicates(subset=["Description", "Adress_check"], inplace=True)
        duplicated_description = rental_df[rental_df["Description"].duplicated()]["Description"].unique().tolist()
        duplicated_address = rental_df[rental_df["Address"].duplicated()]["Address"].unique().tolist()
        drop_duplicate_row(duplicated_description, "Description", "Adress_check", rental_df)
        drop_duplicate_row(duplicated_address, "Address", "Description_check", rental_df)

        rental_df["Date"] = rental_df["Date"].apply(lambda x: x.replace("-", "/"))
        rental_df["Date"] = pd.to_datetime(rental_df["Date"], dayfirst=True)

        if os.path.exists('area_region.json'):
            f = open('area_region.json')
            area_list = json.load(f)
            f.close()
        else:
            service = Service()
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://en.wikipedia.org/wiki/Planning_Areas_of_Singapore")
            table = driver.find_elements(By.CSS_SELECTOR, "table.sortable")
            table_body = table[0].find_element(By.CSS_SELECTOR, 'tbody')
            areas = table_body.find_elements(By.CSS_SELECTOR, "tr")
            area_list = {}
            for i in range(len(areas)):
                item = areas[i].find_elements(By.CSS_SELECTOR, "td > a")
                area_list[item[0].text] = item[1].text
            driver.quit()

            with open("area_region.json", "w") as outfile:
                json.dump(area_list, outfile)

        rental_df["Area"] = rental_df["Location"].apply(lambda x: x[x.find("(") + 1:] if x.find("(") != -1 else x)
        rental_df["Area"] = rental_df["Area"].apply(lambda x: x[x.find("(") + 1:-1] if x.find("(") != -1 else x)
        rental_df["Area"] = rental_df["Area"].apply(lambda x: x.replace(")", ""))
        rental_df["Region"] = rental_df["Area"].apply(lambda x: area_list[x])

        rental_df.drop(columns=["Adress_check","Description_check"], inplace=True)
        rental_df.to_csv(f"{path}sg rental(processed).csv", index=False)

