import random
import datetime
from mySQLconnection import get_real_data

# fetch real data from AWS and populate fake data
def generate_accident() -> dict:
    accident_data = get_real_data()

    lat = accident_data['y_gps']
    long = accident_data['x_gps']

    level = random.randint(0, 4)

    # ct stores current time
    ct = datetime.datetime.now()
    # print("current time:-", ct)
    n = random.randint(0, 10)
    # Add 1 minutes to datetime object
    final_time = ct + datetime.timedelta(minutes=n)

    timestamp = str(final_time)

    duration = random.randint(0, 10)
    return {
        'duration' : duration,
        'latitude': lat,
        'longitude': long,
        'level': level,
        'time': timestamp
    }

# print(generate_accident())