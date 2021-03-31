from flask import Flask, request, redirect, make_response, Blueprint, Response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth import is_logged_in
from google_drive import validate
import google_drive

app = Blueprint('links', __name__)

gc = gspread.service_account(filename='credentials.json')

links, authors = {}, {}

@app.route("/_refresh")
def _refresh():
    return refresh('')

@app.route("/_refresh/<preview>/<to>")
@validate
def preview_refresh(preview, to):
    if preview == 'preview':
        ref_res = refresh(to)
        if ref_res.status_code == 301:
            return redirect(f'/preview{ref_res.headers["Location"]}', 301)
    return make_response("Invalid URL.", 500)

@app.route("/_refresh/<to>")
@validate
def refresh(to):
    temp_links, temp_authors = {}, {}
    try:
        gsheet = gc.open_by_key(os.environ.get('SHEET_ID'))
        for entry in gsheet.sheet1.get_all_records():
            temp_links[entry['Shortlink']] = entry['URL']
            temp_authors[entry['Shortlink']] = entry['Creator']
        global links, authors
        links, authors = temp_links, temp_authors
        if to:
            return redirect(f'/{to}', 301)
        return make_response("Links updated.", 200)
    except Exception as e:
        print(e)
        return make_response("Error reading links.", 500)

@app.route('/<path:shortlink>')
@google_drive.validate
def go(shortlink):

    if shortlink in links:
        if links[shortlink]:
            return redirect(links[shortlink])
        return 'Link missing. Please follow the instructions on the spreadsheet.'
    else:
        return 'Link not found'

@app.route('/preview/<path:shortlink>')
@validate
def preview(shortlink):
    if shortlink in links:
        return f'Points to <a href="{links[shortlink]}">{links[shortlink]}</a> by {authors[shortlink] if authors[shortlink] else "N/A"}'
    else:
        return 'Link not found'
