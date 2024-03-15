from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory, jsonify
import json
import plotly
import plotly.graph_objects as go
import atexit
import requests
from datetime import datetime
from keys import ENDGRATE_API_KEY

app = Flask(__name__) # defines web application
app.config['SECRET_KEY'] = 'acad04e0262e72720856b95f9b9e74a2990314e0009e8d36' # creates secret key

APPLICATION_URL = "https://6m3g4p-5000.csb.app/"

payload = {
    "configuration_webhook": { "endpoint": f"{APPLICATION_URL}callback" },
    "provider": "googleanalytics",
    "schema": [{ "endgrate_type": "analytics-page_analytics" }]
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {ENDGRATE_API_KEY}"
}

response = requests.post("https://endgrate.com/api/pull/initiate", json=payload, headers=headers)

ENDGRATE_SESSION_ID = response.json()["session_id"]
print(f"Endgrate Session ID: {ENDGRATE_SESSION_ID}")

AUTHENTICATED = False
LAST_FETCH = None
OLD_DATA = None


def get_endgrate_data():
    global LAST_FETCH
    global OLD_DATA
    if LAST_FETCH != None:
        t = (datetime.now() - LAST_FETCH)
        if t.seconds/60 <= 5:
            return OLD_DATA
    LAST_FETCH = datetime.now()

    payload = {
        "session_id": ENDGRATE_SESSION_ID,
        "endgrate_type": "analytics-page_analytics",
        "synchronous": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {ENDGRATE_API_KEY}"
    }

    response = requests.post("https://endgrate.com/api/pull/transfer", json=payload, headers=headers)

    
    transfer_id = response.json()["transfer_id"]

    url = f"https://endgrate.com/api/pull/data?endgrate_type=analytics-page_analytics&transfer_id={transfer_id}"

    response = requests.get(url, headers={"accept": "application/json","authorization": f"Bearer {ENDGRATE_API_KEY}"})

    data = response.json()

    pathes = {}



    OLD_DATA = response.json()

    return response.json()

def delete_session():
    import requests

    payload = { "session_id": f"{ENDGRATE_SESSION_ID}" }

    requests.post("https://endgrate.com/api/session/delete", json=payload, headers=headers)

@app.route("/get_data")
def get_data():
    data = get_endgrate_data()
    return jsonify(data)
    
    
@app.route('/callback', methods=["POST"])
def endgrate_callback():
    global AUTHENTICATED
    AUTHENTICATED = True
    return "OK"

@app.route('/auth')
def auth():
    return redirect("https://endgrate.com/session?session_id=" + ENDGRATE_SESSION_ID)

@app.route('/') # home page
def index():
    return render_template('index.html')

@app.route('/google_analytics') # google analytics
def google_analytics():
    if AUTHENTICATED:
        return render_template('google_analytics.html', do_auth=False) #return output page
    
    return render_template('google_analytics.html', do_auth=True) #return output page

if __name__ == '__main__':
    app.run(debug=True) # run application

atexit.register(delete_session) # delete session on exit