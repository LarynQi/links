import os
import json

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
