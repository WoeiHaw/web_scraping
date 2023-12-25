import pandas as pd
import spacy
import json
import os
from datetime import datetime


class ProcessData:
    def __init__(self, path, country):
        self.path = path
        self.country = country
        self.i =0;

    def check_relevant_job(self, detail):
        key_words = ["data", "data analyst", "machine learning", "ai", "artificial intelligence",
                     "business intelligent", "python", "big data", "Developer"]
        detail = detail.lower()
        for key_word in key_words:
            if key_word in detail:
                return True
        return False

    def extract_key_words(self, description):

        nlp = spacy.load('en_core_web_lg')
        places_name = ["Singapore", "Malaysia", "Kuala Lumpur", "Job Requirements", "TikTok", "ByteDance", "Resso",
                       "Interested", "PERSOLKELLY Singapore Pte Ltd"]
        important_key_word = ["Python", "R", "SQL", 'PowerBI', 'Java', "Dash", "python", "MongoDB", "MySQL",
                              "Data-driven", "Data Driven",
                              "Visualization", "visualization", "Excel", "ETL", "BigData", "Machine Learning", "AI",
                              "Artificial Intelligence", "Business Intelligent", "ML", "NLP", "nlp", "ai", "English",
                              "Mandarin"]
        key_words = []
        doc = nlp(description)
        if doc.ents:
            for word in doc.ents:
                if (word.label_ not in ["DATE", "TIME", "MONEY", "CARDINAL", "QUANTITY", "ORDINAL", "GPE"]) & (
                        word.text not in places_name):
                    #                 print(word.text, ent.label_)
                    key_words.append(word.text)
        for token in doc:

            if (token.text in important_key_word) & (token.text not in key_words):
                if token.text == "Power BI":
                    key_words.append("PowerBI")
                elif token.text == "visualization":
                    key_words.append("Visualization")
                elif token.text == "python":
                    key_words.append("Python")
                elif token.text == "nlp":
                    key_words.append("NLP")
                elif token.text == "ai":
                    key_words.append("AI")
                else:
                    key_words.append(token.text)
        return list(set(key_words))

    def find_states_my(self, location):
        f = open('states-cities.json')
        cities_list = json.load(f)
        f.close()

        loc = location.split(",")[1].strip() if len(location.split(",")) > 1 else location.split(",")[0].strip()
        loc = "Pulau Pinang" if (loc == "Penang") | (loc == "Bayan Lepas") | (loc == "Penang - Others") else loc
        loc = "Georgetown" if loc == "George Town" else loc
        loc = "Selangor" if (loc == "Shah Alam/Subang") | (loc == "Klang/Port Klang") | (loc == "Puchong") | (
                loc == "Cyberjaya") | (loc == "Kajang/Bangi/Serdang") | (loc == "Ampang") | (
                                    loc == "Selangor - Others") else loc
        loc = "Johor" if loc == "Johor - Others" else loc
        loc = "Negeri Sembilan" if loc == "Negeri Sembilan - Others" else loc
        if loc == "Kuala Lumpur":
            return loc
        if loc in cities_list.keys():
            return loc
        for key, val in cities_list.items():
            if loc in val:
                return key
        return "Other"

    def process_region_sg(self, area):
        region_list = []
        loc = area.split(",")[1].strip() if len(area.split(",")) > 1 else area.split(",")[0].strip()
        loc = loc.replace("Region", "").replace("- Others", "").strip()
        loc = "North-East" if loc == "North-Eastern Islands" else loc
        f = open('area_region.json')
        region_list = json.load(f)
        f.close()

        if loc in ["North-East", "East", "Central", "West", "North"]:
            return loc
        elif loc in region_list.keys():
            return region_list[loc]
        return "Others"

    def process_data(self):

        if os.path.exists(f"{self.path}{self.country} Job(Processed).csv"):
            current_process_data = pd.read_csv(f"{self.path}{self.country} Job(Processed).csv")
            current_process_data["Date"] = pd.to_datetime(current_process_data["Date"])

        else:
            current_process_data = pd.DataFrame()

        job_df = pd.read_csv(f"{self.path}{self.country} Job.csv")
        job_df["Date"] = pd.to_datetime(job_df["Date"], dayfirst=True)

        if len(current_process_data) != 0:
            current_datetime = datetime.now()
            today_date = current_datetime.date()

            job_df = job_df.query("Date == @today_date")

        job_df.dropna(subset=["Title"], inplace=True)

        job_df["is job related(Title)"] = job_df["Title"].apply(
            lambda x: "Yes" if self.check_relevant_job(x) == True else "No")
        job_df["is job related(Description)"] = job_df["Job Description"].apply(
            lambda x: "Yes" if self.check_relevant_job(x) == True else "No")

        job_df = job_df[(job_df["is job related(Title)"] == 'Yes') & (job_df["is job related(Description)"] == 'Yes')]
        job_df["Posted Date"] = job_df["Posted Date"].apply(lambda x: x.replace("Posted on", ""))
        job_df.drop_duplicates(subset=["Title", "Company Name", "Job Description"], inplace=True)
        for index, row in job_df.iterrows():
            posted_date = row["Posted Date"].replace(" ", "")
            ind = posted_date.find("ago")

            if ind != -1:
                if posted_date[ind-1] == "+":
                    job_df.loc[index, "Posted Date"] = row["Date"] - pd.Timedelta(days=30)
                elif posted_date[ind - 1] != "d":
                    job_df.loc[index, "Posted Date"] = row["Date"]
                elif posted_date[ind-1] == "+":
                    job_df.loc[index, "Posted Date"] = row["Date"] - pd.Timedelta(days=30)
                else:
                    index_d = posted_date.find("dago")

                    days = posted_date[index_d - 2:index_d]
                    if not days.isnumeric():
                        days = posted_date[index_d - 1:index_d]
                    days = int(days)
                    job_df.loc[index, "Posted Date"] = row["Date"] - pd.Timedelta(days=days)

        job_df["Posted Date"] = pd.to_datetime(job_df["Posted Date"], dayfirst=True)
        job_df["Posted Date"] = job_df["Posted Date"].apply(lambda x: x.date())
        job_df["Key Words"] = job_df["Job Description"].apply(self.extract_key_words)

        if self.country == "Malaysia":
            job_df["State/Region"] = job_df["Country/Location"].apply(self.find_states_my)

        elif self.country == "Singapore":
            job_df["State/Region"] = job_df["Country/Location"].apply(self.process_region_sg)

        job_df["Country/Location"] = job_df["Country/Location"].apply(
            lambda x: x.split(",")[0] if len(x.split(",")) > 1 else x)
        job_df.drop(columns=["is job related(Title)", "is job related(Description)"], inplace=True)

        if len(current_process_data) != 0:
            job_df = pd.concat([current_process_data, job_df])

        job_df.drop_duplicates(subset=["Title", "Company Name", "Job Description"], inplace=True)
        job_df.to_csv(f"{self.path}{self.country} Job(Processed).csv", index=False)

        return job_df
