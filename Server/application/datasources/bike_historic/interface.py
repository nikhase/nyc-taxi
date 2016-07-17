import urllib2
import json
import datetime as dt
import treelib
import numpy
from dateutil import parser
from geopy import distance

def searchGoogle(args):
    '''
    Getting the estimate travel time for biking in minutes
    :param args:
    :return:
    '''

    try:
        url = "https://maps.googleapis.com/maps/api/directions/json?"
        url += "origin=" + str(args['start_lat']) + "," + str(args['start_lon'])
        url += "&destination=" + str(args['dest_lat']) + "," + str(args['dest_lon'])
        url += "&mode=bicycling&key=AIzaSyBHC6Nr7Kc2ZmleRmejUWewAAz8FV738vg"
        print url

        response = urllib2.urlopen(url)
        data = json.load(response)
        tripTimeSecs = data['routes'][0]['legs'][0]['duration']['value']
        tripTime = dt.timedelta(seconds=tripTimeSecs)
    except Exception as e:
        time = dt.timedelta(minutes=0, seconds=0, hours=0)
        return str(time)

    return str(tripTime)


# Search Using the Treelib
def search(args):
    # treeImport()
    start = args['start_lat'], args['start_lon']
    dest = args['dest_lat'], args['dest_lon']

    dist = distance.vincenty(start, dest).miles
    '''['pickup_datetime_day', 'pickup_datetime_dayofweek', 'pickup_datetime_hour',
    'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude',
    'trip_time_in_mins']'''

    #2013-01-07 07:43:03.013168+00:00
    timestamp = parser.parse(args['timestamp'])
    val = []
    #val.append(numpy.float64(timestamp.day))
    val.append(numpy.float64(timestamp.weekday()))
    val.append(numpy.float64(timestamp.hour))
    val.append(numpy.float64(args['start_lat']))
    val.append(numpy.float64(args['start_lon']))
    val.append(numpy.float64(args['dest_lat']))
    val.append(numpy.float64(args['dest_lon']))

    res = treelib.getEstimatedTime(val)
    result = {}

    hours = float(dist / res[0])
    minutes = hours * 60.0
    #print "Prediction in hours: " + str(hours)
    result= str(dt.timedelta(minutes=int(minutes)))
    return result