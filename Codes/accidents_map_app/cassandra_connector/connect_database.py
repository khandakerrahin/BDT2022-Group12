from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import datetime
import timedelta
  

cloud_config= {
        'secure_connect_bundle': 'secure-connect-bdt-accidents.zip'
}

auth_provider = PlainTextAuthProvider('XOsLEOoeawEZrZbWztghdatC', 'q1LviFk7Mu0mdNgNYzrwUsZGqcmmIe56vPzAtyco,_0MRNLwp9Ebi+EWAZdnUbPiSYDtBodnHXlzDQwzLIzfhbtzQwxa6PzNzDgnoxIUZpLJdgaRsoFuGWXEmep3Zx9I')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# ct stores current time
ct = datetime.datetime.now()
# print("current time:-", ct)
n =121
# Add 1 minutes to datetime object
final_time = ct - datetime.timedelta(minutes=n)

# print("current time:-", str(ct))
# print("sub time:-", final_time)
 
query = "select * from accident_keyspace.accidents where time > ? ALLOW FILTERING;"

print(query)

pStatement = session.prepare(query)
rows = session.execute(pStatement, [final_time])

# rows = session.execute("select release_version from system.local").one()


for row in rows:
    print(row)


