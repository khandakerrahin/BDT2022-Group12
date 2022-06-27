import folium
import os
import json
from datetime import datetime
import random
import time

def get_current_datetime_string():
    # datetime object containing current date and time
    now = datetime.now()

    # print("now =", now)

    # ddmmYY_HMS
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    # print("date and time =", dt_string)

    return dt_string

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
        lat = accident['lat']
        long = accident['long']
        level = level_array[random.randint(0, 4)]

        logoIcon = folium.features.CustomIcon('car.png', icon_size=(25, 50))

        # Create markers
        folium.Marker([(lat-0.01), (long-0.01)],
                popup='<strong>Car One</strong>',
                tooltip=tooltip,
                icon=logoIcon).add_to(m),


        # Create custom marker icon
        logoIcon = folium.features.CustomIcon('danger.png', icon_size=(50, 50))

        # Create markers
        folium.Marker([lat, long],
                    popup='<strong>Location One</strong>',
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




    # Geojson overlay
    # folium.GeoJson(overlay, name='trentino').add_to(m)

    # Generate map
    m.save('templates/map.html')



if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    
    while True:
        # Generate a map
        generate_map()
        
        print(f'Generating Map @ {datetime.now()}')
        
        # Sleep for a random number of seconds
        time_to_sleep = random.randint(1, 5)
        time.sleep(time_to_sleep)