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

if 'credentials.json' not in os.listdir():
    from utils import gen_credentials
    gen_credentials()

gc = gspread.service_account(filename='credentials.json')

links, authors, dates = {}, {}, {}

@app.route("/_refresh")
def _refresh():
    return refresh('')

@app.route("/_refresh/<preview>/<to>")
@validate
def preview_refresh(preview, to):
    if preview == 'preview':
        ref_res = refresh(to)
        if ref_res.status_code == 302:
            return redirect(f'/preview{ref_res.headers["Location"]}', code=302)
    return make_response("Invalid URL", 404)

@app.route("/_refresh/<to>")
@validate
def refresh(to):
    temp_links, temp_authors, temp_dates = {}, {}, {}
    try:
        gsheet = gc.open_by_key(os.environ.get('SHEET_ID'))
        for entry in gsheet.sheet1.get_all_records():
            shortlink = entry['Shortlink']
            temp_links[shortlink] = entry['URL']
            temp_authors[shortlink] = entry['Creator']
            temp_dates[shortlink] = entry['Date']
        global links, authors, dates
        links, authors, dates = temp_links, temp_authors, temp_dates
        if to:
            return redirect(f'/{to}', 302)
        return make_response("Links updated.", 200)
    except gspread.exceptions.APIError as e:
        if e.response.status_code == 403:
            return make_response(f'Please share {os.environ.get("SHEET_NAME")} with {os.environ.get("SERVICE_EMAIL")}.', 403) 
        return make_response('Error reading links.', 500)
    except KeyError as e:
        return make_response(f'Please do not modify the column names on the spreadsheet', 403) 
    except Exception as e:
        return make_response("Error reading links.", 500)

@app.route('/<path:shortlink>')
@validate
def go(shortlink):
    if shortlink in links:
        if links[shortlink]:
            return redirect(links[shortlink], 302)
        return make_response('Link missing. Please follow the instructions on the spreadsheet.', 403)
    else:
        refresh('')
        if shortlink in links:
            return go(shortlink)
        return make_response('Link not found', 404)

@app.route('/preview/<path:shortlink>')
@validate
def preview(shortlink):
    if shortlink in links:
        return f'<div> Points to <a href="{links[shortlink]}">{links[shortlink]}</a></div> <div> Created by {authors[shortlink] if authors[shortlink] else "N/A"} on {dates[str(shortlink)] if dates[str(shortlink)] else "N/A"} </div>'
    else:
        refresh('')
        if shortlink in links:
            return preview(shortlink)
        return make_response('Link not found', 404)
