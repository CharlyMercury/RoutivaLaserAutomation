from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
import json


class GoogleDriveUtilities:

    def __init__(self, folder_id_):
        self.cred_token_write = False
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile("./src/google_drive_code/my_creds.json")

        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("./src/google_drive_code/my_creds.json")

        # Creates local webserver and auto
        # handles authentication.
        self.drive = GoogleDrive(self.gauth)

        # replace the value of this variable
        # with the absolute path of the directory
        self.folder_id = folder_id_
        self.file_id = ''

    def download_file(self, file_name_: str):

        file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(self.folder_id)}).GetList()

        if len(file_list) == 0:
            return False
        elif len(file_list) > 0:
            for i, file in enumerate(sorted(file_list, key=lambda y: y['title']), start=1):
                print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
                try:
                    self.file_id = file['id']
                    file.GetContentFile(file['title'])
                    os.rename(file_name_, f'./gcodes/{file_name_}')
                    return True, "Download Successfully"
                except Exception as err:
                    print(err)
                    return False, err

    def remove_file_gdrive(self):
        try:
            file = self.drive.CreateFile({'id': self.file_id})
            file.Delete()
            return True, "Removed Successfully"
        except Exception as err:
            print(err)
            return False, err

    def create_token_file(self, cred_token):
        with open("./src/google_drive_code/my_creds.json", "w") as outfile:
            json.dump(cred_token, outfile)
        self.cred_token_write = True

    def delete_token_file(self):
        os.remove("./src/google_drive_code/my_creds.json")
        self.cred_token_write = False


"""folder_id = '1Clv8oI2A3zdSZeqg5oFlXGLsxFN6GhKL'
file_name = 'pedido_31_ago.gcode'
google_drive_ = GoogleDriveUtilities(folder_id)
print(google_drive_.download_file(file_name))
print(google_drive_.remove_file_gdrive())
"""