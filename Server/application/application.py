import datasources.taxi_realtime.interface as rt_taxi
import datasources.taxi_historic.interface as hist_taxi
import datasources.bike_historic.interface as bike_hist
import geopy.distance as distance
import price
import datetime as dt

def search(args):
    '''

    :param args:
    :return:
    '''

    result = {}
    taxi = {}
    bike = {}
    taxi['realtime'] = rt_taxi.search(args)
    taxi['historic'] = hist_taxi.search(args)
    bike['historic'] = bike_hist.search(args)

    # Need distance and time estiamtion for pricing estimation
    dist = distanceEstimation(args)
    carTime = dt.datetime.strptime(taxi['realtime'],"%H:%M:%S.%f").minute
    bikeTime = dt.datetime.strptime(bike['historic'],"%H:%M:%S").minute
    result['prices'] = price.price_estimation(args['timestamp'], dist, carTime, bikeTime)
    result['taxi'] = taxi
    result['bike'] = bike

    return result


def distanceEstimation(args):
    '''
    Estimate the road distance between two points
    :param args: dictionary containing 'start_lat', 'start_lon', 'dest_lat' & 'dest_lon',
    :return: Road Distance estimation
    '''


    start = args['start_lat'], args['start_lon']
    dest = args['dest_lat'], args['dest_lon']
    atob = distance.vincenty(start, dest).miles

    # Usage of circuity concepts to derive roadmap distance
    # Source: http://www.sciencedirect.com/science/article/pii/S0965856401000441
    atob *= 1.2
    return atob



#Testing Stuff
'''
Coordinates = {}
# Define Start
Coordinates['start_lat'] = 40.751573
Coordinates['start_lon'] = -73.991857

# Define End
Coordinates['dest_lat'] = 40.770475
Coordinates['dest_lon'] = -73.879504
Coordinates['timestamp'] = str(dt.datetime.now())

results = search(Coordinates)
'''