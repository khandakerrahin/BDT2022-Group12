import json
import mysql.connector

# connect to a database hosted on AWS
db = mysql.connector.connect(
    host=HOST,
    user=USERID,
    password=PASSWORD,
    database=DBNAME
)

cursor = db.cursor(dictionary=True)

def get_real_data():

    cursor.execute("SELECT y_gps, x_gps FROM accidents ORDER BY RAND() LIMIT 1;")
    for row in cursor:
        return row

