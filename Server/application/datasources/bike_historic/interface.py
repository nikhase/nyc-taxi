import urllib2
import json
import datetime as dt



def search(args):
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
        raise e

    return str(tripTime)