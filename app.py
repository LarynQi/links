import functools
import json
import os
import flask
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
import google_drive
import links

app = flask.Flask(__name__)

app.secret_key = os.environ.get('FN_FLASK_SECRET_KEY', default=False)

# https://www.mattbutton.com/2019/01/05/google-authentication-with-python-and-flask/
app.register_blueprint(google_auth.app)
app.register_blueprint(google_drive.app)
app.register_blueprint(links.app)

@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + user_info['given_name'] + '</div><pre>' + json.dumps(user_info, indent=4) + '</pre>'
    return '<button onclick="window.location.href=\'\\login\';"> Login </button>'
