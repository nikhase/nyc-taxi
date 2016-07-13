from flask import Flask, request, jsonify
from Components import Listener, GraphHandler, Refresher
import copy
import datetime as dt
import threading
import utils.queries as queries
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/duration")
def duration():
    lock = threading.Lock();
    lock.acquire()

    try:
        rad = float(request.args.get('r'))
        params = {}
        params['start_lat'] = float(request.args.get('lta'))
        params['start_lon'] = float(request.args.get('lga'))

        params['dest_lat'] = float(request.args.get('ltb'))
        params['dest_lon'] = float(request.args.get('lgb'))

        print params
        graph.lock()
        graphCopy = copy.deepcopy(graph.g)

        graph.unlock()
        lock.release()

        query = queries.duration(params['start_lat'], params['start_lon'] , params['dest_lat'], params['dest_lon'], radius=rad)
        results = graphCopy.query(query)
        print "Graph size: " + str(graphCopy.__len__())
        dictResults = []
        for result in results:
            res = {}
            res['duration'] = str(result[0])
            res['start_lat'] = str(result[1])
            res['start_long'] = str(result[2])
            res['dest_lat'] = str(result[3])
            res['dest_long'] = str(result[4])
            dictResults.append(res)

        return jsonify(results = dictResults)

    except IOError:
        return "Error"


if __name__ == "__main__":
    basetime = dt.datetime.strptime("2013-01-07T00:00:00", "%Y-%m-%dT%H:%M:%S")
    b = Listener(IP="127.0.0.1", Port=5005)
    r = Refresher(sleep=60)
    graph = GraphHandler(b, cache_size=10, basetime=basetime)
    graph.addObservable(r)
    #app.debug = True
    try:
        app.run(threaded=True)
    except IOError:
        print ("IOError")
        pass


    #Central Park
    #Start Lat: 40.766564
    #Start Lon: 73.979788

    #Empire State
    #Dest Lat: 40.749071
    #Dest Lon: 73.986118

