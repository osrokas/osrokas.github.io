from flask import Flask, render_template

app = Flask(__name__)

import requests
import urllib3
import folium
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from folium import PolyLine
import pandas as pd
from pandas.io.json import json_normalize
import webbrowser


auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "48610",
    'client_secret': '04546ee3949e18d0e64c6e1824cc27490330360f',
    'refresh_token': '99ddf411219f6f9cba38e96b784fe55986aa9c29',
    'grant_type': "refresh_token",
    'f': 'json'
}

res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']


header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()
act = json_normalize(my_dataset)

def decode_polyline(polyline_str):
    '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs'''
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']: 
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates





@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template("portfolio.html")

@app.route('/CV')
def CV():
    return render_template("about_me.html")

@app.route('/marsrutas')
def marsrutas():
    return render_template("marsrutas.html")

@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')

@app.route('/heatmap_time')
def heatmap_time():
    return render_template("keliones_pagal_laika.html")

@app.route('/keliones')
def keliones():
    return render_template("mano_citybee.html")
    
@app.route('/notebook_citybee')
def notebook_citybee():
    return render_template("notebook_citybee.html")

@app.route('/mapsas')
def mapsas():


   
    m = folium.Map([54.732940, 25.237409],
                tiles="OpenStreetMap",
                zoom_start=10)
    i = 0

    act["coord"] = ''
    listas = []
    for a in act['map.summary_polyline']:
        c = decode_polyline(a)
        listas.append(c)

    run = folium.FeatureGroup("Run")
    ride = folium.FeatureGroup("Ride")
    ski = folium.FeatureGroup("Ski")

    i = 0
    for b in listas: 
        act["coord"][i] = b
        i=i+1
        
    act_run = act.loc[(act['type'] == 'Run')]
    act_bike = act.loc[(act['type'] == 'Ride')]
    act_ski = act.loc[(act['type'] == 'BackcountrySki')]


    for index, row in act_run.iterrows():
        folium.PolyLine(row['coord'], color='green', line_weight=5, tooltip=row.type, opacity = 0.6, dash_array='8',
        popup= folium.Popup(row.type +"  " + row.start_date,  max_width=500, min_width=200)).add_to(run)
        

    for index, row in act_bike.iterrows():
        folium.PolyLine(row['coord'], color='red', line_weight=5, tooltip=row.type, opacity = 0.6, dash_array='8',
        popup= folium.Popup(row.type +"  " + row.start_date,  max_width=500, min_width=200)).add_to(ride)

        
    for index, row in act_ski.iterrows():
        folium.PolyLine(row['coord'], color='blue', line_weight=5, tooltip=row.type, opacity = 0.6, dash_array='8',
        popup= folium.Popup(row.type +"  " + row.start_date,  max_width=500, min_width=200)).add_to(ski)

        

        

    run.add_to(m)
    ride.add_to(m)
    ski.add_to(m)


    folium.LayerControl().add_to(m)




    return m._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)