import pandas as pd


class Backup:
    def __init__(self, file_location, backup_location):
        self.file_location = file_location
        self.backup_location = backup_location

        if len(file_location) == len(backup_location):
            for i in range(len(file_location)):
                data_to_save = pd.read_csv(file_location[i])
                data_to_save.to_csv(backup_location[i], index=False)
        else:
            print("Backup not success. Please make sure that the length of file_location and "
                  "backup_location are the same")
