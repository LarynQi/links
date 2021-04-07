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

from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

import secrets

app = flask.Flask(__name__)

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.secret_key = os.environ.get('FN_FLASK_SECRET_KEY', default=False)

app.register_blueprint(google_auth.app)
app.register_blueprint(google_drive.app)
app.register_blueprint(links.app)

@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        key = secrets.token_urlsafe(64)
        google_auth.recv_key(flask.request.cookies.get('session'), key)
        return flask.make_response('<h1>Codebase Links</h1> <div> You are currently logged in as <b>' + user_info["name"] + '</b></div><br> ' + f'<div><img src="{user_info["picture"]}" /></div>' + f'<div><p>Authorized: <b>{google_drive.is_validated()}</b></p</div>' + f'<div><button onclick="window.location.href=\'\\logout\\?key={key}\';"> Logout </button></div>', 200)
    return flask.make_response('<h1>Codebase Links</h1> <div><button onclick="window.location.href=\'\\login\';"> Login </button></div>', 200)

csrf = CSRFProtect()
csrf.init_app(app)

SELF = "'self'"

csp = {
    'default-src': SELF,
    'img-src': '*'
}

Talisman(app, content_security_policy=csp)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
