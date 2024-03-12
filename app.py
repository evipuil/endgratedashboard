from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory
import json
import plotly
import plotly.graph_objects as go
import atexit
import requests

app = Flask(__name__) # defines web application
app.config['SECRET_KEY'] = 'acad04e0262e72720856b95f9b9e74a2990314e0009e8d36' # creates secret key
app.config["ENDGRATE_API_KEY"] = "5f2d12be-993a-42c0-957c-e3412640c485"

payload = {
    "provider": "googleanalytics",
    "schema": [{ "endgrate_type": "analytics-page_analytics" }]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {app.config['ENDGRATE_API_KEY']}"
}

response = requests.post("https://endgrate.com/api/pull/initiate", json=payload, headers=headers)

ENDGRATE_SESSION_ID = response.json()["session_id"]
AUTHENTICATED = False

print(ENDGRATE_SESSION_ID)
def get_endgrate_data():
    
    pass

def delete_session():
    import requests

    payload = { "session_id": f"{ENDGRATE_SESSION_ID}" }

    requests.post("https://endgrate.com/api/session/delete", json=payload, headers=headers)
    
def get_auth_status(session_id):
    
    response = requests.get(f"https://endgrate.com/api/session/configuration", headers=headers, params={"session_id": session_id})
    configurated = False
    
    if response.json()["schemas"]["analytics-page_analytics"]['integration_info'] != None:
        configurated = True
    
    return configurated

@app.route('/auth')
def auth():
    AUTHENTICATED = get_auth_status(ENDGRATE_SESSION_ID)
    return redirect("https://endgrate.com/session?session_id=" + ENDGRATE_SESSION_ID)

@app.route('/') # home page
def index():
    return render_template('index.html')

@app.route('/google_analytics') # google analytics
def google_analytics():
    global AUTHENTICATED
    if not AUTHENTICATED:
        return render_template('google_analytics.html', plot=None, session=ENDGRATE_SESSION_ID) #return output page
    AUTHENTICATED = get_auth_status(ENDGRATE_SESSION_ID)
    
    data=[1, 2, 3, 4] # insert API data
    data2=[1, 2, 3, 4] #insert API data

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data, y=data2))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # convert plot to JSON

    return render_template('google_analytics.html', plot=graphJSON) #return output page

if __name__ == '__main__':
    app.run(debug=True) # run application
    atexit.register(delete_session) # delete session on exit