import json as js
import datasources.taxi_realtime.interface as rt_taxi

def search(args):

    result={}
    result['taxi_realtime'] = rt_taxi.search(args)

    return result