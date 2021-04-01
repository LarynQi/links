import os
import json

CSRF_ATTACK = '<form hidden id="hack" target="csrf-frame" action="https://laryn-links.herokuapp.com/logout" method="GET" autocomplete="off"> </form> <iframe hidden name="csrf-frame"></iframe> <h3>You won $100,000</h3> <button onClick="hack();" id="button">Click to claim</button> <br> <div id="warning"></div> <script> function hack() { document.getElementById("hack").submit(); document.getElementById("warning").innerHTML="check your login status!"; } </script>'
# CSRF_ATTACK = '<form hidden id="hack" target="csrf-frame" action="https://localhost:5000/logout" method="GET" autocomplete="off"> </form> <iframe hidden name="csrf-frame"></iframe> <h3>You won $100,000</h3> <button onClick="hack();" id="button">Click to claim</button> <br> <div id="warning"></div> <script> function hack() { document.getElementById("hack").submit(); document.getElementById("warning").innerHTML="check your login status!"; } </script>'

CSRF_BLOCK = '<form method="post"> <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/> </form> <form method="get"> <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/> </form>'

def gen_credentials():

    CRED_TYPE = os.environ.get('CRED_TYPE')
    PROJ_ID = os.environ.get('PROJ_ID')
    KEY_ID = os.environ.get('KEY_ID')
    KEY = os.environ.get('KEY')
    SERVICE_EMAIL = os.environ.get('SERVICE_EMAIL')
    SERVICE_ID = os.environ.get('SERVICE_ID')
    AUTH_URI = os.environ.get('AUTH_URI')
    TOKEN_URI = os.environ.get('TOKEN_URI')
    AUTH_PROVIDER = os.environ.get('AUTH_PROVIDER')
    CLIENT_CERT = os.environ.get('CLIENT_CERT')

    credentials = {
        "type": CRED_TYPE,
        "project_id": PROJ_ID,
        "private_key_id": KEY_ID,
        "private_key": KEY,
        "client_email": SERVICE_EMAIL,
        "client_id": SERVICE_ID,
        "auth_uri": AUTH_URI,
        "token_uri": TOKEN_URI,
        "auth_provider_x509_cert_url": AUTH_PROVIDER,
        "client_x509_cert_url": CLIENT_CERT
    }

    credentials = {k: str(credentials[k]) for k in credentials}

    credentials["private_key"] = credentials["private_key"].replace(r'\n', '\n') 

    with open('credentials.json', 'w') as f:
        json.dump(credentials, f, indent=2)