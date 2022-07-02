import json
import urllib.request

# This method is used to fetch the accident records for last minute
def get_records_last_minute():
        accident_list = urllib.request.urlopen("http://34.238.136.151/").read()
        my_json = accident_list.decode('utf8').replace("'", '"')
        return json.loads(my_json)

# This method is used to fetch the accident records history for last 5 minutes
def get_count_last_five_minutes():
        accident_counts = urllib.request.urlopen("http://34.238.136.151/fetch_last_five").read()
        my_json = accident_counts.decode('utf8').replace("'", '"')
        return json.loads(my_json)