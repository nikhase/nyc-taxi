#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request, abort, send_from_directory, Response
import application.application as ap
from RealtimeDB.realtimedb import RealtimeDB
import datetime as dt


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def get_info():


    # Example Query:
    # http://localhost:5000/search?lta=40.770475&lga=-73.879504&ltb=40.751573&lgb=-73.991857
    try:
        # Get the Search Parameters
        params = {}
        params['start_lat'] = request.args.get('lata')
        params['start_lon'] = request.args.get('lga')

        params['dest_lat'] = request.args.get('latb')
        params['dest_lon'] = request.args.get('lgb')
        params['timestamp'] = dt.datetime.now()

        try:
            if not hardcodedResult:

                delta = dt.datetime.now() - rtdb.initTimestamp
                basetime = rtdb.graph.baseTime + delta * streamspeed
                params['timestamp'] = str(basetime)
                result = ap.search(params)
                result['info'] = params
            else:

                # Create Hard Coded Result
                result ={}
                taxi = {}
                taxi['historic'] = "00:08:55"
                taxi['realtime'] = "00:10:12"
                taxi['price'] = "12,25USD"
                bike = {}
                bike['historic'] = "00:18:55"
                bike['price'] = "1,00USD"
                info = {}
                info = params;
                result['taxi'] = taxi
                result['bike'] = bike
                result['info'] = info
                print result

        except Exception as e:
            print str(e)
            return abort(500)

        if not result is None:
            return jsonify(result)
        else:
            return abort(500)

    except IOError:
        return badRequest("Sorry, one of the parameters was not submitted correctly!")


# Return a 400 with a customized message
def badRequest(message ='No Error message!'):
    # Transfer message
    data = message

    # Return message in template
    return render_template('400_temp.html', data = data)


# Start server
if __name__ == '__main__':
    # Flag to use Realtime Data
    realtime = False
    streamspeed= 2
    # Flag to use hard coded result for frontend testing
    hardcodedResult = True

    # @@@Server needs to keep track of time

    if realtime:
        # Location for the csv File
        path = "/Users/larshelin/Documents/Studium/Master/Semester 3/Seminar/Data/oneweekfrom20130107.csv"

        # Configures, Start and Runs the Realtime Data stream
        rtdb = RealtimeDB(path, startIndex=50000, rows=20000, speed=streamspeed, reset=True)

    #app.debug = True
    app.run()