import json as js
import datasources.taxi_realtime.interface as rt_taxi
#import datasources.taxi_historic.interface as hist_taxi

def search(args):

    result={}
    result['taxi_realtime'] = rt_taxi.search(args)
    #result['taxi_historic'] = hist_taxi.search(args)

    return result