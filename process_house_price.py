import pandas as pd
import json
import os
from datetime import datetime
from datetime import timedelta

class ProcessHousePrice:
    def __init__(self, path, city):
        self.path = path
        self.city = city

    def process_size(self, size):
        index = size.find("Acres")
        size = size.replace("sq.ft.", "")
        if index == -1:
            return float(size)
        else:
            size = size.replace("Acres", "").strip()

            size = float(size)
            if size >= 10:
                return size

            return size * 43560

    def remove_outliers(self, df):
        # remove outlier for size
        Q1 = df['Size (sq.ft)'].quantile(0.25)
        Q3 = df['Size (sq.ft)'].quantile(0.75)
        IQR = Q3 - Q1

        threshold = 3
        outliers = df[
            (df['Size (sq.ft)'] < Q1 - threshold * IQR) | (df['Size (sq.ft)'] > Q3 + threshold * IQR)]
        df = df.drop(outliers.index)

        df = df[df["Size (sq.ft)"] > 50]
        df["Price"] = df["Price"].apply(lambda x: float(x.replace(",", "")))
        df["Price/Sq.ft"] = round(df["Price"] / df["Size (sq.ft)"], 2)

        threshold_ = 1.5
        Q1_ = df['Price/Sq.ft'].quantile(0.25)
        Q3_ = df['Price/Sq.ft'].quantile(0.75)
        IQR_ = Q3_ - Q1_

        outliers_ = df[
            (df['Price/Sq.ft'] < Q1_ - threshold_ * IQR_) | (df['Price/Sq.ft'] > Q3_ + threshold_ * IQR_)]
        df = df.drop(outliers_.index)

        return df

    def find_location_jb(self, location, type_):
        f = open('johor_bahru.json')
        parliament_state_list = json.load(f)
        f.close()

        other_places = ["PONTIAN", "BATU PAHAT", "KOTA TINGGI", "KLUANG", "MUAR", "SIMPANG RENGGAM", "MERSING",
                        "TANGKAK",
                        "MERSING", "AYER HITAM", "SEGAMAT", "PEKAN NANAS", "YONG PENG", "DESARU", "BANDAR PENAWAR"]

        if type(location) == float:
            return ""

        location = location.upper().replace("'", "").replace("ASUTIN", "AUSTIN").replace("TERBAU", "TEBRAU").replace(
            "TERBU", "TEBRAU") \
            .replace("’", "").replace("TMN", "TAMAN").replace("UNIVERISITI", "UNIVERSITI").replace("DATO OON",
                                                                                                   "DATO ONN").replace(
            "EKO", "ECO") \
            .replace("AUSITN", "AUSTIN").replace("MOUST", "MOUNT").replace("DATO ON", "DATO ONN").replace("UNIVERISTI",
                                                                                                          "UNIVERSITI") \
            .replace("MOUTH", "MOUNT").replace("TAMAM", "TAMAN").replace("UNIVERSITY", "UNIVERSITI").replace("MITIARA",
                                                                                                             "MUTIARA") \
            .replace("TWINS RESIDENCE", "TWIN RESIDENCE").replace("EKO BOTANI", "EKO BOTANIC")

        for place in other_places:
            if place in location:
                return "no relevant"

        if "UDA UTAMA" in location:
            location = "BANDAR UDA UTAMA"
        elif "TWIN GALAXY" in location:
            location = "TAMAN ABAD"
        elif "SEASONS LUXURY" in location:
            location = "SEASON LUXURY"
        elif "KSL" in location:
            location = "TAMAN ABAD"
        elif ("TAN SRI YAAKOB" in location) | ("SRI YAACOB" in location):
            location = "TAN SRI YAACOB"
        elif ("AUSTIN RESIDENCE" in location) | ("Mutiara Emas" in location):
            location = "MOUNT AUSTIN"
        elif "JAYA PUTRA PERDANA" in location:
            location = "JP PERDANA"
        elif "DANGA SUTERA" in location:
            location = "SUTERA UTAMA"
        elif "PONDEROSA" in location:
            location = "TAMAN PONDEROSA"
        elif "ARC" in location:
            location = "DAYA"
        elif ("BISTARI PERDANA" in location) | ("BESTARI PERDANA" in location):
            location = "BANDAR BISTARI PERDANA"
        elif "AUSTIN KIARA" in location:
            location = "AUSTIN HEIGHTS"
        elif "KOLAM AIR" in location:
            location = "KOLAM AYER"
        elif "ROS MERAH" in location:
            location = "JOHOR JAYA"

        for parliament in parliament_state_list:
            for state in parliament_state_list[parliament]:
                for area in parliament_state_list[parliament][state]:
                    if (area in location) | (area.replace(" ", "") in location) | (
                            area.replace("HEIGHTS", "HEIGHT") in location) \
                            | (area.replace("HILLS", "HILL") in location) | ((area.replace("SERI", "SRI") in location)):
                        area = "TAMAN UNGKU TUN AMINAH" if area == "TUN AMINAH" else area
                        area = "SOUTH KEY" if area == "MID VALLEY" else area
                        if type_ == "area":
                            return area
                        elif type_ == "state":
                            return state
                        elif type_ == "parliament":
                            return parliament
        return ""

    def find_location_kl(self, location, type_="area"):
        f = open('kuala_lumpur.json')
        parliament_list = json.load(f)
        f.close()
        if type(location) == float:
            return ""
        location = location.upper().replace("TMN", "TAMAN").replace("BDR", "BANDAR").replace("HEIGHT",
                                                                                             "HEIGHTS").replace("SG",
                                                                                                                "SUNGAI") \
            .replace('DR.', "DR")

        other_places = ["AMPANG", "PETALING JAYA", "WANGSA MELAWATI", "DAMANSARA", "PANDAN JAYA",
                        "BANDAR TUN HUSSIEN ONN",
                        "TAMAN  KERAMAT", "PUCHONG", "PANDAN PERDANA", "TAMAN DAMAI INDAH", "SUNGAI BULOH",
                        "TAMAN BUKIT ANGSANA",
                        "TAMAN LINGKARAN NUR", "TAMAN LAGENDA MAS", "SHAH ALAM", "GOMBAK", "TAMAN BUKIT HATAMAS",
                        "ULU KELANG",
                        "SILK RESIDENCE", "TAMAN MAWAR", "HULU LANGAT", "TAMAN MINANG RIA", "TAMAN SIERRA UKAY",
                        "TAMAN LEMBAH MAJU",
                        "CHERAS", "PANDAN", "SELANGOR", "TUN HUSSIEN ONN", "PUTRAJAYA", "KAJANG", "TAMAN PERMATA",
                        "TUN HUSSEIN ONN",
                        "MELAWATI", "SRI DAMASARA", "LEMBAH KERAMAT", "TAMAN DAYA", "PORT DICKSON", "SEREMBAN",
                        "TAMAN KERAMAT",
                        "KERAMAT"]
        for place in other_places:
            if place in location:
                if ("KERAMAT WANGSA" in location) | ("DATUK KERAMAT" in location):
                    continue
                return "no relevant"
        if "MIHARJA" in location:
            location = "TAMAN MIHARJA"
        if "IBUKOTA" in location:
            location = "TAMAN IBU KOTA"

        for parliament in parliament_list:
            for area in parliament_list[parliament]:
                if area in location:
                    if type_ == "area":
                        return area
                    elif type_ == "parliament":
                        return parliament
        return ""

    def process(self):
        if os.path.exists(f"{self.path}House Price {self.city}(Processed).csv"):
            current_process_data = pd.read_csv(f"{self.path}House Price {self.city}(Processed).csv")
            current_process_data["Date"] = pd.to_datetime(current_process_data["Date"], dayfirst=True, format="mixed")
        else:
            current_process_data = pd.DataFrame()
        price_df = pd.read_csv(f"{self.path}House Price {self.city}.csv")
        price_df["Date"] = pd.to_datetime(price_df["Date"], dayfirst=True, format="mixed")

        if len(current_process_data) != 0:
            process_datetime = current_process_data["Date"].iloc[-1] + timedelta(days=1)
            process_date = process_datetime.date()
            price_df = price_df.query("Date >= @process_date")
        price_df.dropna(subset=["Size (sq.ft)", "Number of bathroom", "Number of bedroom"], inplace=True)
        price_df = price_df[price_df["Title"] != "Property Wanted"]
        price_df = price_df[price_df["Size (sq.ft)"] != ""]

        mask = price_df["Type"] != 'Warehouse / Factory'
        mask2 = price_df["Type"] != 'Agricultural'

        price_df = price_df.loc[mask]
        price_df = price_df.loc[mask2]

        price_df.drop_duplicates(subset=["Title", "Type", "Number of bathroom", "Number of bedroom", "Price"],
                                 inplace=True)
        price_df["Size (sq.ft)"] = price_df["Size (sq.ft)"].apply(self.process_size)
        price_df = self.remove_outliers(price_df)

        price_df.drop(price_df[price_df["Number of bathroom"] == "-"].index, inplace=True)
        price_df["Number of bathroom"] = price_df["Number of bathroom"].apply(
            lambda x: 10 if x == "More than 10" else 10 if x == "10+" else int(x))

        price_df["Number of bedroom"] = price_df["Number of bedroom"].apply(
            lambda x: 0 if (len(x) > 5) | (x == "-") else x)
        price_df["Number of bedroom"] = price_df["Number of bedroom"].apply(
            lambda x: 10 if x == "More than 10" else int(float(x)))
        price_df.drop(price_df[price_df["Number of bedroom"] == 0].index, inplace=True)

        if self.city == "JB":
            price_df["Area"] = price_df["Address"].apply(lambda x: self.find_location_jb(x, "area"))
            mask = price_df["Area"] == ""
            price_df.loc[mask, "Area"] = price_df.loc[mask, "Title"].apply(lambda x: self.find_location_jb(x, "area"))
            price_df = price_df[price_df["Area"] != "no relevant"]

            price_df["State"] = price_df["Address"].apply(lambda x: self.find_location_jb(x, "state"))
            mask = price_df["State"] == ""
            price_df.loc[mask, "State"] = price_df.loc[mask, "Title"].apply(lambda x: self.find_location_jb(x, "state"))

            price_df["Parliament"] = price_df["Address"].apply(lambda x: self.find_location_jb(x, "parliament"))
            mask = price_df["Parliament"] == ""
            price_df.loc[mask, "Parliament"] = price_df.loc[mask, "Title"].apply(
                lambda x: self.find_location_jb(x, "parliament"))
            price_df["Area"] = price_df["Area"].apply(lambda x: "Undefined" if x == "" else x)
            price_df["State"] = price_df["State"].apply(lambda x: "Undefined" if x == "" else x)
            price_df["Parliament"] = price_df["Parliament"].apply(lambda x: "Undefined" if x == "" else x)
        elif self.city == "kl":
            price_df["Area"] = price_df["Address"].apply(lambda x: self.find_location_kl(x, "area"))
            mask = price_df["Area"] == ""
            price_df.loc[mask, "Area"] = price_df.loc[mask, "Title"].apply(self.find_location_kl)
            price_df = price_df[price_df["Area"] != "no relevant"]

            price_df["Parliament"] = price_df["Address"].apply(lambda x: self.find_location_kl(x, "parliament"))
            mask2 = price_df["Parliament"] == ""
            price_df.loc[mask2, "Parliament"] = price_df.loc[mask2, "Title"].apply(
                lambda x: self.find_location_kl(x, "parliament"))

            price_df.loc[price_df["Area"] == "", "Area"] = "Undefined"
            price_df.loc[price_df["Parliament"] == "", "Parliament"] = "Undefined"

        if len(current_process_data) != 0:
            price_df = pd.concat([current_process_data, price_df])

        price_df.drop_duplicates(subset=["Title", "Type", "Number of bathroom", "Number of bedroom", "Price"],
                                 inplace=True)
        price_df["Date"] = price_df['Date'].dt.strftime('%d/%m/%Y')
        price_df.to_csv(f"{self.path}House Price {self.city}(Processed).csv", index=False)
