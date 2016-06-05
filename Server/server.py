#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request, abort, send_from_directory, Response
import application.application as ap
from RealtimeDB.realtimedb import RealtimeDB

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def get_info():

    try:
        # Get the Search Parameters
        params = {}
        params['start_lat'] = request.args.get('lta')
        params['start_lon'] = request.args.get('lga')

        params['dest_lat'] = request.args.get('ltb')
        params['dest_lon'] = request.args.get('lgb')

        result = ap.search(params)

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
    # Flag to use realtime Data
    realtime = False

    if realtime:
        # Location for the csv File
        path = "/Users/larshelin/Documents/Studium/Master/Semester 3/Seminar/Data/oneweekfrom20130107.csv"

        # Configures, Start and Runs the Realtime Data stream
        RealtimeDB(path, startIndex=50000, rows=20000, speed=2, reset=True)

    # app.debug = True
    app.run()