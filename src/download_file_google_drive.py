"""
    Google Drive File Downloader for Laser Cutting Machine GCode

    This Python module facilitates the seamless downloading of a GCode file from Google Drive,
        which serves as input for a laser cutting machine.

    Features:

        Authentication: The module facilitates passing Google Drive credentials for authentication
            and access acquisition.

        Download Management: Provides methods for downloading the GCode file and managing its GDrive deletion
            once the download is complete.

        Credential Management: Offers two methods for managing credentials
            - one to create credentials in a JSON file and another to delete them after usage for enhanced security.
"""
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
import json
import logging


class GoogleDriveUtilities:

    def __init__(self, folder_id_, credentials_):
        """
            Class Constructor: GoogleDriveUtilities

                This constructor initializes an instance of the GoogleDriveUtilities class.

            :param folder_id_: folder_id_: Identifier of the Google Drive Folder from
                which the GCode files will be downloaded.
            :param credentials_: Temporary credentials required for authenticating with
                Google Drive to access the specified folder.
        """
        self.folder_id = folder_id_
        self.create_token_file(credentials_)
        self.file_id = ''
        self.cred_token_write = False
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile("./src/google_drive_code/my_creds.json")
        self.drive = GoogleDrive(self.gauth)

    def download_file(self, file_name_: str = "") -> tuple:
        """
            Method: download_file

                This method facilitates the downloading of a file from Google Drive.

            :param file_name_: The name of the file to be downloaded from Google Drive.
            :return: A tuple containing the download status (success/failure)
                and a message indicating the result of the download process.
        """
        file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(self.folder_id)}).GetList()

        if len(file_list) == 0:
            return False, "Download Failed"
        elif len(file_list) > 0:
            logging.info("Download in progress")
            for i, file in enumerate(sorted(file_list, key=lambda y: y['title']), start=1):
                # print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
                try:
                    self.file_id = file['id']
                    file.GetContentFile(file['title'])
                    os.rename(file_name_, f'./gcodes/{file_name_}')
                    return True, "Download Successfully"
                except Exception as err:
                    print(err)
                    return False, err

    def remove_file_gdrive(self) -> tuple:
        """
            Method: remove_file_gdrive

                This method removes the downloaded file from GoogleDrive.

            :return: A tuple containing the removal status (success/failure)
                and a message indicating the result of the removal process.
        """
        try:
            file = self.drive.CreateFile({'id': self.file_id})
            file.Delete()
            logging.info("File Removed Successfully")
            return True, "Removed Successfully"
        except Exception as err:
            print(err)
            return False, err

    def create_token_file(self, cred_token) -> None:
        """
        Method: create_token_file

            This method creates a temporary file containing the Google Drive credentials.

        :param cred_token: A dictionary containing the Google Drive credentials.
        :return: None
        """
        with open("./src/google_drive_code/my_creds.json", "w") as outfile:
            json.dump(cred_token, outfile)
        self.cred_token_write = True

    def delete_token_file(self):
        """
        Method: delete_token_file

            This method deletes the temporary file containing the Google Drive credentials.
        """
        os.remove("./src/google_drive_code/my_creds.json")
        self.cred_token_write = False


"""
credentials = {}
folder_id = '1Clv8oI2A3zdSZeqg5oFlXGLsxFN6GhKL'
file_name = 'pedido_31_ago.gcode'
google_drive_ = GoogleDriveUtilities(folder_id, credentials)
print(google_drive_.download_file(file_name))
print(google_drive_.remove_file_gdrive())
google_drive_.delete_token_file()
"""