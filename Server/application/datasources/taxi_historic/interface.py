import treelib
import numpy
import datetime as dt
from dateutil import parser

def search(args):
    # treeImport()
    start = args['start_lat'], args['start_lon']
    dest = args['dest_lat'], args['dest_lon']

    '''['pickup_datetime_day', 'pickup_datetime_dayofweek', 'pickup_datetime_hour',
    'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude',
    'trip_time_in_mins']'''

    #2013-01-07 07:43:03.013168+00:00
    timestamp = parser.parse(args['timestamp'])
    val = []
    val.append(numpy.float64(timestamp.day))
    val.append(numpy.float64(timestamp.weekday()))
    val.append(numpy.float64(timestamp.hour))
    val.append(numpy.float64(args['start_lat']))
    val.append(numpy.float64(args['start_lon']))
    val.append(numpy.float64(args['dest_lat']))
    val.append(numpy.float64(args['dest_lon']))

    res = treelib.getEstimatedTime(val)
    result = {}
    result= str(dt.timedelta(minutes=int(res[0])))
    return result

