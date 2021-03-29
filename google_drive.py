import googleapiclient.discovery
from google_auth import build_credentials, get_user_info, is_logged_in
import flask
import os

app = flask.Blueprint('google_drive', __name__)

def build_drive_api_v3():
    credentials = build_credentials()
    return googleapiclient.discovery.build('drive', 'v3', credentials=credentials).files()

def find_files(filename, _id):
    drive_api = build_drive_api_v3()
    results = drive_api.list(        
        q=f"name='{filename}'", pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    found = False
    for item in items:
        if item['id'] == _id:
            found = True

    return items, found

def is_validated():
    if is_logged_in():
        res = find_files(os.environ.get('SHEET'), os.environ.get('SHEET_ID'))
        return res and res[1]
    return False
