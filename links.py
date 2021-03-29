from flask import Flask, request, redirect, make_response, Blueprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import google_drive

app = Blueprint('links', __name__)

gc = gspread.service_account(filename='credentials.json')

links, authors = {}, {}

# @app.route("/")
# def base():
#     return redirect("https://codebase.berkeley.edu/")

@app.route("/_refresh")
def _refresh():
    return refresh('')

@app.route("/_refresh/<to>")
def refresh(to):
    if google_drive.is_validated():
        # gsheet = gc.open_by_key('1wj_zxh7pJ_ZDiAVEudPrQyUJCUC9vsyNgWY9fbWsHgc')
        temp_links, temp_authors = {}, {}
        try:
            gsheet = gc.open_by_key('1xdEJFmJrOmBYbqi0MyYyY_pcNjzi7wXLXaBfA0rMmp0')
            for entry in gsheet.sheet1.get_all_records():
                temp_links[entry['Shortlink']] = entry['URL']
                temp_authors[entry['Shortlink']] = entry['Creator']
            global links, authors
            links, authors = temp_links, temp_authors
            if to:
                return redirect(f'/{to}')
            return make_response("Links updated.", 200)
        except Exception as e:
            print(e)
            return make_response("Error reading links.", 500)
    return redirect('/login/_refresh')
    # return redirect('/login?redirect=_refresh')

@app.route('/<path:shortlink>')
def go(shortlink):
    if google_drive.is_validated():
        if shortlink in links:
            return redirect(links[shortlink])
        else:
            return 'Link not found'
    return redirect(f'/login/{shortlink}')
    # return redirect(f'/login?redirect={shortlink}')

@app.route('/preview/<path:shortlink>')
def preview(shortlink):
    if google_drive.is_validated():
        if shortlink in links:
            return f'Points to <a href="{links[shortlink]}">{links[shortlink]}</a> by {authors[shortlink] if authors[shortlink] else "N/A"}'
        else:
            return 'Link not found'
    return redirect(f'/login/{shortlink}')
    # return redirect(f'/login?redirect={shortlink}')

# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

