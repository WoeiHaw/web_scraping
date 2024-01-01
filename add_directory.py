import os

class AddDirectory:
    def __init__(self):
        path = "./"
        folders = ["assets","data","Data_back_up"]
        for folder in folders:

            folder_path = f"{path}{folder}"
            if not os.path.exists(folder_path) :
                os.makedirs(folder_path)
                if folder =="assets":
                    os.makedirs(f"{folder_path}/shoes images my")
                    os.makedirs(f"{folder_path}/shoes images sg")


