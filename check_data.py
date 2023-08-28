import pandas as pd
from datetime import datetime

TODAY_DATE = datetime.now().strftime("%d-%m-%Y")


class Check_data():
    def __init__(self, file_name):
        self.nan_column = []
        try:
            data = pd.read_csv(file_name)

            data["Date"] = data["Date"].apply(lambda x: x.replace("/","-"))
            #now = pd.to_datetime(TODAY_DATE, format="%d-%m-%Y")

            today_data = data[data["Date"] == TODAY_DATE]

            for column in today_data:
                if today_data[column].isnull().sum() !=0:
                    self.nan_column.append(column)
            if len(today_data) == 0:
                self.is_today_empty =True
            else:
                self.is_today_empty = False
        except FileNotFoundError:
            self.is_today_empty = True


