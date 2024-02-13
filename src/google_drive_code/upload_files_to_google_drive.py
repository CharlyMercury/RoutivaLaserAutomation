# Useful url: https://www.projectpro.io/recipes/upload-files-to-google-drive-using-python
# Useful url: https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf
# Useful url: https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process


from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# Below code does the authentication
# part of the code
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.json")


if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.json")

# Creates local webserver and auto
# handles authentication.
drive = GoogleDrive(gauth)

# replace the value of this variable
# with the absolute path of the directory
upload_file_list = [r'proposed_architecture.png', r'proposed_architecture_2.png']
folder_id = '1Clv8oI2A3zdSZeqg5oFlXGLsxFN6GhKL'

# iterating thought all the files/folder
# of the desired directory
for x in upload_file_list:
    file_ = drive.CreateFile({'parents': [{'id': folder_id}]})
    file_.SetContentFile(x)
    file_.Upload()

    # Due to a known bug in pydrive if we
    # don't empty the variable used to
    # upload the files to Google Drive the
    # file stays open in memory and causes a
    # memory leak, therefore preventing its
    # deletion

    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()

    for file_2 in file_list:
        print('title: %s, id: %s' % (file_2['title'], file_2['id']))

    for i, file_3 in enumerate(sorted(file_list, key=lambda y: y['title']), start=1):
        print('Downloading {} file from GDrive ({}/{})'.format(file_3['title'], i, len(file_list)))
        file_3.GetContentFile(file_3['title'])