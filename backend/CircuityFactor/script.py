import geopy.distance as distance
import pandas as pd
import csv
import json
import urllib2



# https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=AIzaSyBHC6Nr7Kc2ZmleRmejUWewAAz8FV738vg

def googleDistance(args):
    try:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        url += "origins=" + str(args['start_lat']) + "," + str(args['start_lon'])
        url += "&destinations=" + str(args['dest_lat']) + "," + str(args['dest_lon'])
        url += "&key=AIzaSyBHC6Nr7Kc2ZmleRmejUWewAAz8FV738vg"
        #print url
        return 0
        #response = urllib2.urlopen(url)
        #data = json.load(response)
        return data['rows'][0]['elements'][0]['distance']['value']

    except Exception as e:
        return 0


path="/Users/larshelin/Documents/Studium/Master/Semester 3/Seminar/Data/oneweekfrom20130107.csv"
df = pd.read_csv(path, nrows=2200)sum = 0
n  = 0

dict = {}
dict['start_lat'] = []
dict['start_lon']= []
dict['dest_lat'] = []
dict['dest_lon'] = []
dict['euclidian'] = []
dict['real'] = []
dict['start_timestamp'] = []
dict['dest_timestamp'] = []

for i in range(99,2100):
    row = df.ix[i]
    args = {}
    args['start_lat'] = row['pickup_latitude']
    args['start_lon']  = row['pickup_longitude']
    args['dest_lat']  = row['dropoff_latitude']
    args['dest_lon'] = row['dropoff_longitude']

    start = args['start_lat'], args['start_lon']
    dest = args['dest_lat'], args['dest_lon']

    #Skip identical locations
    if dest == start:
        continue

    #Skip identical times
    if row['pickup_datetime'] == row['dropoff_datetime']:
        continue

    euclidian = distance.vincenty(start,dest).meters
    #print str(euclidian)
    real = googleDistance(args)
    #print real
    if real == 0:
        continue

    dict['start_lat'].append(str(args['start_lat']))
    dict['start_lon'].append(str(args['start_lon']))
    dict['dest_lat'].append(str(args['dest_lat']))
    dict['dest_lon'].append(str(args['dest_lon']))
    dict['start_timestamp'].append(row['pickup_datetime'])
    dict['dest_timestamp'].append(row['dropoff_datetime'])
    dict['euclidian'].append(euclidian)
    dict['real'].append(real)

    #circuity = real / euclidian
    #sum += circuity
    n += 1

with open("test.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(dict.keys())
   writer.writerows(zip(*dict.values()))