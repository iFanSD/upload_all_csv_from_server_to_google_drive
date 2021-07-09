from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pprint as pp
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('drive', 'v3', credentials=creds)


def create_folder_in_gd(folder_id_location='0AEEWu43XWUKEUk9PVA', name_of_folder="New Folder"):
    """Creating new folder in Google Drive"""
    file_metadata = {
        'name': name_of_folder,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id_location]
    }
    r = service.files().create(body=file_metadata,
                               fields='id').execute()
    pp.pprint(r)
    return r['id']

def upload_to_gd_folder(folder_id, file_path, name_of_file, type=None):
    """Uploading files to Google Drive"""
    file_metadata = {
        'name': name_of_file,
        'mimeType': type,
        # text/csv - for example or 'application/vnd.google-apps.spreadsheet' for transformation csv to google_sheet
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    pp.pprint(r)



if __name__ == '__main__':
    folder_path='/home/ifansd/all/'
    folder_id_created = create_folder_in_gd(name_of_folder="all_test4")
    for name_of_file in os.listdir(folder_path):
        upload_to_gd_folder(name_of_file=name_of_file, folder_id=folder_id_created,type='text/csv',file_path=f'{folder_path}{name_of_file}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
