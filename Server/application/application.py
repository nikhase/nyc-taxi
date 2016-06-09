import json as js
import datasources.taxi_realtime.interface as rt_taxi
import datasources.taxi_historic.interface as hist_taxi

def search(args):

    result={}
    taxi = {}
    taxi['realtime'] = rt_taxi.search(args)
    taxi['historic'] = hist_taxi.search(args)
    taxi['price'] = "Unknown"

    result['taxi'] = taxi
    return result