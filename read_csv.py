import pandas as pd


class Read_csv():
    def __init__(self, filename):
        try:
            self.data = pd.read_csv(f"{filename}")
        except FileNotFoundError:
            self.data = pd.DataFrame()

    def get_links(self):
        link_column = ""

        if len(self.data) == 0:
            return []
        else:
            # global link_column
            for column in self.data:
                count = 0
                if len(self.data) < 10:
                    num_sample = len(self.data)
                else:
                    num_sample = 10
                column_check = self.data[column].sample(num_sample)

                for i in range(len(column_check)):

                    if type(column_check.iloc[i]) == str:
                        if column_check.iloc[i].find("https:") == -1:
                            break
                        count += 1

                        if count == num_sample:
                            link_column = column
                            break
            return self.data[link_column].tolist()

    def get_jobid(self):
        if len(self.data) == 0:
            return []
        else:
            return self.data["Job ID"].tolist()
