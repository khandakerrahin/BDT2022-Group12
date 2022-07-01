import json
import mysql.connector

# connect to a database hosted on AWS
db = mysql.connector.connect(
    host='accidentsdb.cz6av9bkf3xq.eu-west-3.rds.amazonaws.com',
    user='Admin2',
    password='bdtproject2022',
    database='accidentsDB'
)

cursor = db.cursor(dictionary=True)

# Fetch Real data from AWS to polulate fake data
def get_real_data():

    cursor.execute("SELECT y_gps, x_gps FROM accidents ORDER BY RAND() LIMIT 1;")
    for row in cursor:
        return row

