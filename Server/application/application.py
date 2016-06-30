import datasources.taxi_realtime.interface as rt_taxi
import datasources.taxi_historic.interface as hist_taxi
import datasources.bike_historic.interface as bike_hist
import datasources.miscellaneous.walking as walking
import geopy.distance as distance
import price
import calories
import datetime as dt

def search(args):
    '''

    :param args:
    :return:
    '''

    result = {}
    taxi = {}
    bike = {}
    walk = {}
    taxi['realtime'] = rt_taxi.search(args)
    taxi['historic'] = hist_taxi.search(args)
    bike['historic'] = bike_hist.search(args)
    walk['estimation'] = walking.search(args)

    # Need distance and time estiamtion for pricing estimation
    dist = distanceEstimation(args)



    if taxi['realtime'] == "0:00:00":
        carEstimation = taxi['historic']
    else:
        carEstimation = taxi['realtime']

    # Travel Times needed for price calculation
    carTime = dt.datetime.strptime(carEstimation,"%H:%M:%S").minute
    bikeTime = dt.datetime.strptime(bike['historic'],"%H:%M:%S").minute

    # Get the calories
    cals = calories.calories(dist, bikeTime)
    result['calories'] = cals
    result['taxi'] = taxi
    result['bike'] = bike
    result['walking'] = walk
    result['estimated_distance'] = ("%.2f" % dist)


    # Get the prices
    result['prices'] = price.price_estimation(args['timestamp'], dist, carTime, bikeTime)


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

    #print start
    #print dest
    #print str(atob)
    # Usage of circuity concepts to derive roadmap distance
    # Source: http://www.sciencedirect.com/science/article/pii/S0965856401000441
    # Actual Value based on research using ~1950 trips an compare to distance from google
    atob *= 1.416
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
print results'''