import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Backup_drive():
    def __init__(self, path):

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        fileName = ["Darlie Toothpaste", "Dettol Shower Gel", "House Price JB", "House Price kl",
                    "kopi o price", "Malaysia Job", "Nivea Man", "sg rental",
                    "shampoo price", "Singapore Job", "skechers_shoes_MY", "skechers_shoes_SG", "sg rental(processed)",
                    "Singapore Job(Processed)", "Malaysia Job(Processed)", "House Price kl(Processed)",
                    "House Price JB(Processed)"]
        folder_list = drive.ListFile(
            {
                'q': "title='Data_back_up'  and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        folder_id = folder_list[0]['id']

        file_query = f"'{folder_id}' in parents and trashed=false"
        file_list = drive.ListFile({'q': file_query}).GetList()

        for file1 in file_list:

            if file1['title'].replace(".csv", "") in fileName:
                file1.Delete()

        for name in fileName:
            f = drive.CreateFile({'title': f"{name}.csv",
                                  'mimeType': 'text/csv',
                                  "parents": [{"kind": "drive#fileLink", "id": "1JEp79t-I3f0QI-3mgLQ1phTh-ht26vqy"}]})
            f.SetContentFile(f"{path}{name}.csv")
            f.Upload()

        # Due to a known bug in pydrive if we
        # don't empty the variable used to
        # upload the files to Google Drive the
        # file stays open in memory and causes a
        # memory leak, therefore preventing its
        # deletion
        f = None

        assets_folder_list = drive.ListFile(
            {
                'q': f"title='assets' and '{folder_id}' in parents  and mimeType='application/vnd.google-apps.folder' "
                     f"and trashed=false"}).GetList()
        if assets_folder_list:
            assets_folder_id = assets_folder_list[0]['id']
        else:
            folder_metadata = {'title': "assets", 'mimeType': 'application/vnd.google-apps.folder',
                               'parents': [{"id": folder_id}]}
            drive_folder = drive.CreateFile(folder_metadata)
            drive_folder.Upload()
            assets_folder_list = drive.ListFile(
                {
                    'q': f"title='assets' and '{folder_id}' in parents and "
                         "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
            assets_folder_id = assets_folder_list[0]['id']

        for folder_name in os.listdir("./assets"):
            image_folder = drive.ListFile(
                {
                    'q': f"'{assets_folder_id}' in parents and title = '{folder_name}'"
                }
            ).GetList()

            if not image_folder:

                image_folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder',
                                         'parents': [{"id": assets_folder_id}]}
                image_folder = drive.CreateFile(image_folder_metadata)
                image_folder.Upload()

            folder_path = os.path.join("./assets", folder_name)
            local_images = [image for image in os.listdir(folder_path)]
            image_folder_id = drive.ListFile(
                {
                    'q': f"title = '{folder_name}' and '{assets_folder_id}' in parents"
                }
            ).GetList()[0]['id']

            image_list = drive.ListFile(
                {
                    "q": f"'{image_folder_id}' in parents "
                         # f"and mimeType contains 'image/'"
                }
            ).GetList()

            drive_images = [image['title'] for image in image_list]
            upload_image = []
            for image in local_images:
                if image not in drive_images:
                    upload_image.append(image)

            for image in upload_image:
                file_path = os.path.join(folder_path, image)
                file_drive = drive.CreateFile({"title": image, 'parents': [{'id': image_folder_id}]})
                file_drive.SetContentFile(file_path)
                file_drive.Upload()
