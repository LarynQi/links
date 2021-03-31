# links

A secure shortlink server inspired by CS61A's Link Servers ([links](https://github.com/Cal-CS-61A-Staff/links), [shortlinks](https://github.com/Cal-CS-61A-Staff/cs61a-apps/tree/master/shortlinks))

## Local Setup

1. Create a virtualenv

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. Environment variables

<ins>Google Oauth & Flask App</ins>
- `FN_AUTH_REDIRET_URI`
- `FN_BASE_URI`
- `FN_CLIENT_ID`
- `FN_CLIENT_SECRET`
- `FN_FLASK_SECRET_KEY`

_See [this guide](https://www.mattbutton.com/2019/01/05/google-authentication-with-python-and-flask/)_

<ins>Google Sheets API</ins> (can be substitude with `credentials.json`)
- `CRED_TYPE`
- `PROJ_ID`
- `KEY_ID`
- `KEY`
- `SERVICE_EMAIL`
- `SERVICE_ID`
- `AUTH_URI`
- `TOKEN_URI`
- `AUTH_PROVIDER`
- `CLIENT_CERT`

_Enable Google Sheets API and download `credentials.json` from [GCP](https://console.cloud.google.com/apis/library)_

<ins>Private Link Spreadsheet</ins>
- `SHEET_NAME`
- `SHEET_ID`

_Create Google Spreadsheet from the following [template](https://docs.google.com/spreadsheets/d/1LxHmJcAtCzqim-ptH81oNaZMpM3s9CkIGlFS6phe1A8/edit?usp=sharing)_

3. Run

```sh
python3 app.py
```

The `links` app will be listening at [http://localhost:5000/](http://localhost:5000/)

## Development

1. In development, add `debug=True` as a keyword argument to `app.run` in `app.py`. Remove before deploying to production.