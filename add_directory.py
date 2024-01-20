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
                if not os.path.exists(f"{folder_path}/shoes images my"):
                    os.makedirs(f"{folder_path}/shoes images my")
                if not os.path.exists(f"{folder_path}/shoes images sg"):
                    os.makedirs(f"{folder_path}/shoes images sg")


