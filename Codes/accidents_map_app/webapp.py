from flask import Flask, send_from_directory, render_template
import folium
import os
import json
from datetime import datetime
import random
import time
import csv
from cassandra_connector.connect_database import get_records_last_minute, get_count_last_five_minutes

app = Flask(__name__)

# This is used for generating a map with all the data plotted as markers
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


  # fetch location coordinates from Cassandra
  data = get_records_last_minute()


  # Iterating through all the records to add them on the map         
  for accident in data:
      lat = accident['lat']
      long = accident['long']
      level = level_array[accident['level']]

      
      # generating random car markers
      logoIcon = folium.features.CustomIcon('car.png', icon_size=(25, 50))

      folium.Marker([(lat-0.01*(random.randint(-4, 4))), (long-0.01*(random.randint(-4, 4)))],
              popup='<strong>Car</strong>',
              tooltip=tooltip,
              icon=logoIcon).add_to(m),


      # Plotting the Accident data
      logoIcon = folium.features.CustomIcon('danger.png', icon_size=(50, 50))

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


# This is the root directory, it loads the template and fetch data
@app.route('/')
def load_home():
  map_html = generate_map()
  with open('templates/index.html', 'r') as f:
    html_string = f.read()
  # print("Before: ", html_string)
  accident_history = get_count_last_five_minutes()

  print(accident_history)
  with open('templates/hist.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(accident_history)
  
  replaced_html = html_string.replace("replace_me_map", map_html)
  replaced_html = replaced_html.replace("replace_me_counts", str(accident_history))
  # print("After: ", html_string)
  return replaced_html

@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('templates', path)

if __name__ == '__main__':
  app.run(host='0.0.0.0')