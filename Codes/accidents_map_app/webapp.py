from flask import Flask, send_from_directory, render_template
import folium
import os
import json
from datetime import datetime
import random
import time

app = Flask(__name__)


@app.route('/generate_map')
def generate_map():
  # Create map object
  # UniTN Department of Sociology and Social Research Co-ordinates
  m = folium.Map(location=[46.0666, 11.1195], zoom_start=13)

  # Global tooltip
  tooltip = 'Accident'

  # Danger level color palette
  level_01 = '#fff600'
  level_02 = '#ffc302'
  level_03 = '#ff8f00'
  level_04 = '#ff5b00'
  level_05 = '#ff0505'

  level_array = ['#fff600', '#ffc302', '#ff8f00', '#ff5b00', '#ff0505']
  # read location coordinates
  filename = "data/acc_json.json"
  with open(filename, encoding="utf8") as f:
      data = json.load(f)

  # print("Length:", len(data))
              
  for accident in data:
      # print(accident)
      lat = accident['lat']-0.01*(random.randint(-4, 4))
      long = accident['long']-0.01*(random.randint(-4, 4))
      level = level_array[random.randint(0, 4)]

      logoIcon = folium.features.CustomIcon('car.png', icon_size=(25, 50))

      # Create markers
      folium.Marker([(lat-0.01*(random.randint(-4, 4))), (long-0.01*(random.randint(-4, 4)))],
              popup='<strong>Car</strong>',
              tooltip=tooltip,
              icon=logoIcon).add_to(m),


      # Create custom marker icon
      logoIcon = folium.features.CustomIcon('danger.png', icon_size=(50, 50))

      # Create markers
      folium.Marker([lat, long],
                  popup='<strong>Location</strong>',
                  tooltip=tooltip,
                  icon=logoIcon).add_to(m),

      # Circle marker
      folium.CircleMarker(
          location=[(lat-0.000001), (long-0.000001)],
          radius=50,
          popup='ACC',
          color=level,
          fill=True,
          fill_color=level,
          fill_opacity=0.5,
          icon=logoIcon
      ).add_to(m)
  
  return m._repr_html_()

@app.route('/')
def load_home():
  map_html = generate_map()
  with open('templates/index.html', 'r') as f:
    html_string = f.read()
  # print("Before: ", html_string)
  replaced_html = html_string.replace("replace_me", map_html)   
  # print("After: ", html_string)
  return replaced_html

@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('templates', path)

if __name__ == '__main__':
  app.run(host='0.0.0.0')