from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import datetime
import timedelta
  
# Configuring the authentication parameters for Cassandra hosted in Astra DataStax
cloud_config= {
        'secure_connect_bundle': 'cassandra_connector/secure-connect-bdt-accidents.zip'
}

auth_provider = PlainTextAuthProvider('XOsLEOoeawEZrZbWztghdatC', 'q1LviFk7Mu0mdNgNYzrwUsZGqcmmIe56vPzAtyco,_0MRNLwp9Ebi+EWAZdnUbPiSYDtBodnHXlzDQwzLIzfhbtzQwxa6PzNzDgnoxIUZpLJdgaRsoFuGWXEmep3Zx9I')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# This method is used to fetch the accident records for last minute
def get_records_last_minute():

        # ct stores current time
        ct = datetime.datetime.now()
        # print("current time:-", ct)
        n = 121
        # Add 1 minutes to datetime object
        final_time = ct - datetime.timedelta(minutes=n)

        # print("current time:-", str(ct))
        # print("sub time:-", final_time)
        
        query = "select latitude, longitude, level from accident_keyspace.accidents where time > ? ALLOW FILTERING;"

        #print(query)

        pStatement = session.prepare(query)

        rows = session.execute(pStatement, [final_time])

        accident_list = []
        for row in rows:
                #print(row)
                accident_list.append({
                "lat": row[0],
                "long": row[1],
                "level": row[2]
                })
        #print(accident_list)
        return accident_list

# This method is used to fetch the accident records history for last 5 minutes
def get_count_last_five_minutes():

        # ct stores current time
        ct = datetime.datetime.now()
        
        final_time1 = ct - datetime.timedelta(minutes=121)
        final_time2 = ct - datetime.timedelta(minutes=122)
        final_time3 = ct - datetime.timedelta(minutes=123)
        final_time4 = ct - datetime.timedelta(minutes=124)
        final_time5 = ct - datetime.timedelta(minutes=125)

        hist = [final_time1, final_time2, final_time3, final_time4, final_time5]
        
        query = "select count(*) from accident_keyspace.accidents where time > ? ALLOW FILTERING;"

        # print(query)
        accident_counts = []
        pStatement = session.prepare(query)
        for min in hist:
                rows = session.execute(pStatement, [min])

                for row in rows:
                        #print(row)
                        accident_counts.append(row[0])

        #print(accident_counts)
        return accident_counts