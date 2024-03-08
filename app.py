from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory
import json
import plotly
import plotly.graph_objects as go

app = Flask(__name__, static_folder='Static') # defines web application
app.config['SECRET_KEY'] = 'acad04e0262e72720856b95f9b9e74a2990314e0009e8d36' # creates secret key

@app.route('/') # home page
def index():
    return render_template('index.html')

@app.route('/google_analytics') # google analytics
def google_analytics():
    data=[1, 2, 3, 4] # insert API data
    data2=[1, 2, 3, 4] #insert API data

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data, y=data2))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # convert plot to JSON

    return render_template('google_analytics.html', plot=graphJSON) #return output page