import time

import pandas as pd
from datetime import datetime
import os

now = datetime.now()
TODAY_DATE = now.strftime("%d-%m-%Y")


def check_guardian_facewash(filename, new_data):
    if filename == "Nivea Man.csv":
        if "Guardian Price" in new_data:
            if new_data["Guardian Price"].values[0] != "":
                new_data["Guardian Price"] = float(new_data["Guardian Price"].values) * 2

    return new_data


class Save_data():
    def __init__(self, filename, data_save_dict, is_today_empty, shoes_data=False):

        if shoes_data:
            if os.path.exists(filename):
                shoes_df = pd.read_csv(filename)
                shoes_df.loc[len(shoes_df),"Date"] = data_save_dict["Date"][0]
                mask = shoes_df["Date"] == data_save_dict["Date"][0]
                link_df = pd.read_csv(f"data/{filename[-6:-4]} Skechers Link.csv")
                for i in range(len(data_save_dict["Description"])):

                    description = data_save_dict["Description"][i]
                    price = data_save_dict["Price"][i]
                    link = data_save_dict["Link"][i]

                    if description in shoes_df:
                        shoes_df.loc[mask, description] = price
                        link_df.loc[link_df["Description"] == description, "link"] = link
                    else:
                        data_len = len(link_df)
                        shoes_df[description] = ""
                        shoes_df.loc[mask, description] = price
                        link_df.loc[data_len, "Description"] = description
                        link_df.loc[data_len, "link"] = link
            else:
                shoes_df = pd.DataFrame()
                link_df = pd.DataFrame(columns=["Description", "link"])
                shoes_df["Date"] = data_save_dict["Date"][0]
                # mask = shoes_df["Date"] == data_save_dict["Date"][0]
                for i in range(len(data_save_dict["Description"])):
                    description = data_save_dict["Description"][i]
                    price = data_save_dict["Price"][i]
                    link = data_save_dict["Link"][i]

                    shoes_df[description] = price

                    link_df.loc[i, "Description"] = description
                    link_df.loc[i, "link"] = link
            shoes_df.to_csv(filename,index = False)
            link_df.to_csv(f"data/{filename[-6:-4]} Skechers Link.csv",index = False)
        else:
            try:
                data = pd.read_csv(filename)

                new_data = pd.DataFrame(data_save_dict)

                if not is_today_empty:
                    data["Date"] = data["Date"].apply(lambda x: pd.to_datetime(x, dayfirst=True).strftime("%d-%m-%Y"))
                    new_data = check_guardian_facewash(filename, new_data)
                    for column in new_data:
                        if column in data.columns:
                            mask1 = (data["Date"] == TODAY_DATE)
                            data.loc[mask1, column] = new_data[column].values

            except FileNotFoundError:
                data = pd.DataFrame()
                new_data = pd.DataFrame(data_save_dict)

            new_data = check_guardian_facewash(filename, new_data)

            if (len(data) != 0) & (is_today_empty):
                combine_data = pd.concat([data, new_data])
                combine_data["Date"] = combine_data["Date"].apply(
                    lambda x: pd.to_datetime(x, dayfirst=True).strftime("%d-%m-%Y"))
                for i in range(10):
                    try:
                        combine_data.to_csv(filename, index=False)
                        break
                    except PermissionError as error:
                        print(f"Please close file\n{error}")
                        time.sleep(30)
            elif not is_today_empty:

                data["Date"] = data["Date"].apply(lambda x: pd.to_datetime(x, dayfirst=True).strftime("%d-%m-%Y"))

                for i in range(10):
                    try:
                        data.to_csv(filename, index=False)
                        break
                    except PermissionError as error:
                        print(f"Please close file\n{error}")
                        time.sleep(30)

            else:
                new_data.to_csv(filename, index=False)
