import db_access
import json
import geopy.distance as distance
import datetime as dt


def search(args):

    start = args['start_lat'], args['start_lon']
    dest = args['dest_lat'], args['dest_lon']
    atob = distance.vincenty(start, dest).km

    if atob < 2:
        radius = atob / 2
    else:
        radius = 1

    # Get the results
    # Setting radius here, however it is varied within the get Data method starting at 200 meters
    results = json.loads(db_access.getData(args, radius=radius, online=True))

    if len(results) == 0:
        result = dt.timedelta(hours=0, minutes=0, seconds=0, microseconds=0)
        return str(result)

    for res in results:
        # Get start end and point as tuples
        a = res['start_lat'], res['start_long']
        b = res['dest_lat'], res['dest_long']

        # Calculate distance between the results
        dist = distance.vincenty(a, b)

        # Calculate the deviation from the Original Requested location
        deviation = distance.vincenty(a, start).km + distance.vincenty(b, dest).km

        res['deviation'] = deviation
        delta = res['duration']
        res['adjustedDurationS'] = (atob/ dist.km) * int(delta)

    devSum = sum(res['deviation'] for res in results)
    durSum = 0

    # Add up the weighted times
    for res in sorted(results, key=lambda k: k['deviation']):
        alpha = res['deviation'] / devSum
        #print str(alpha)

        # Only one result, weighting is not necessary
        if not alpha == 1:
            durSum += res['adjustedDurationS'] * (1 - alpha)
        else:
            durSum = res['adjustedDurationS']

    # Add Information
    result = {}
    result['estimatedDuration'] = str(dt.timedelta(seconds=int(durSum)))
    result['numberOfResults'] = str(len(results))

    return result['estimatedDuration']


# Testing stuff
'''
params = {}
params['start_lat'] = 40.770475
params['start_lon'] = -73.879504

params['dest_lat'] = 40.751573
params['dest_lon'] = -73.991857


result = search(params)
print result'''