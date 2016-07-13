import pandas as pd
import socket
import time

class streamer:
    def __init__(self, ip, port, dataRoot):
        self._port = port
        self._dataRoot=str(dataRoot)
        self._ip=ip

    def offset(self, startIndex, numOfEvents):
        self._Index = startIndex
        self._numberOfEvent = numOfEvents
        self._nRows = startIndex + numOfEvents

    def start(self, speed_multiplier):

        self._speedMultiplier = float(1) / float(speed_multiplier)

        df = pd.read_csv(self._dataRoot, nrows=self._nRows)
        df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
        df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
        df.sort_values("pickup_datetime")
        df.index = df['pickup_datetime']

        print "UDP target IP:", self._ip
        print "UDP target port:", self._port
        print "Stream speed: ", self._speedMultiplier

        sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP

        for i in xrange(self._Index, self._numberOfEvent+self._Index - 1 ):
            date_1 = df.ix[i][3]
            date_2 = df.ix[i + 1][3]
            diff = ((pd.to_datetime(date_2) - pd.to_datetime(date_1))).seconds * self._speedMultiplier
            msg = str(df.ix[i].to_json(date_format="iso"))
            sock.sendto(msg, (self._ip, self._port))
            time.sleep(diff)
        sock.close()
        print ("Streamer closed")
        return