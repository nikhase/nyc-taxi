import geopy.distance as distance
import datetime as dt

def search(args):
    '''
    Calculates the time to walk from a start- to an endpoint
    :param args:
    :return: Time as stringified timedelta hh:mm:ss
    '''
    # Parameters
    circuityFactor = 1.428082
    avgWalkingSpeed = 3 #mph

    # Start and Endpoints
    start = args['start_lat'], args['start_lon']
    dest = args['dest_lat'], args['dest_lon']

    # Estimate distance based on circuity factor
    dist = distance.vincenty(start, dest).miles * circuityFactor

    # Calculate Time based on average walking speed
    walkingTimeMin = (dist / avgWalkingSpeed ) * 60
    walkiingTime = dt.timedelta(minutes=int(walkingTimeMin))

    return str(walkiingTime)