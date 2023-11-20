from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googleapiclient.discovery import build
import os

class Download_data():
    def __init__(self):
        # Authenticate with PyDrive
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        # Authenticate with Google Drive API
        service = build('drive', 'v3', credentials=gauth.credentials)

        # Specify the folder's ID that you want to download files from
        folder_id = '1JEp79t-I3f0QI-3mgLQ1phTh-ht26vqy'

        # Create a folder on your local machine to save the downloaded files
        local_folder_path = '../../data'
        os.makedirs(local_folder_path, exist_ok=True)

        # List files in the specified folder
        folder_query = f"'{folder_id}' in parents"
        file_list = drive.ListFile({'q': folder_query}).GetList()
        fileName = ["Darlie Toothpaste", "Dettol Shower Gel", "House Price JB", "House Price kl",
                    "kopi o price", "Malaysia Job", "Nivea Man", "sg rental",
                    "shampoo price", "Singapore Job", "skechers_shoes_MY", "skechers_shoes_SG","sg rental(processed)"]

        for file in file_list:
            if file["title"].replace(".csv","") in fileName:

                # Download each file and save it to the local folder
                local_file_path = os.path.join(local_folder_path, file['title'])
                file.GetContentFile(local_file_path)

                print(f"Downloaded: {file['title']}")

        print("All files downloaded to the local folder.")
