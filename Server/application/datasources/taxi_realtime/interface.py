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
    results = json.loads(db_access.getData(args, radius=radius, online=True))
    print str(results)

    if len(results) == 0:
        return "no result found"

    for res in results:
        # Get start end and point as tuples
        a = res['start_lat'], res['start_long']
        b = res['dest_lat'], res['dest_long']

        # Calculate distance between the results
        dist = distance.vincenty(a, b)

        # Calculate the deviation from the Original Requested location
        deviation = distance.vincenty(a, start) + distance.vincenty(b, dest)

        res['deviation'] = deviation
        t = dt.datetime.strptime(res['duration'], "%H:%M:%S")
        delta = dt.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        res['adjustedDurationS'] = (atob/ dist.km) * delta.seconds

    devSum = sum(res['deviation'].km for res in results)
    durSum = 0

    # Add up the weighted times
    for res in sorted(results, key=lambda k: k['deviation']):
        alpha = res['deviation'].km / devSum
        durSum += res['adjustedDurationS'] * alpha

    # Add Information
    result = {}
    result['estimatedDuration'] = str(dt.timedelta(seconds=durSum))
    result['numberOfResults'] = str(len(results))

    return result


# Testing stuff
'''
params = {}
params['start_lat'] = 40.770475
params['start_lon'] = -73.879504

params['dest_lat'] = 40.751573
params['dest_lon'] = -73.991857


result = search(params)'''
