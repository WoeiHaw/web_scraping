from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Backup_drive():
    def __init__(self):

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        path = "../../data/"

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
