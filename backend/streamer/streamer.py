import pandas as pd
import socket
import time

class streamer:
    def __init__(self, ip, port, dataRoot):
        self._port = port
        self._dataRoot=str(dataRoot)
        self._ip=ip




    def start(self, speed_multiplier):

        self._speedMultiplier = speed_multiplier

        df = pd.read_csv(self._dataRoot, nrows=1000)
        df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
        df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
        df.sort_values("pickup_datetime")
        df.index = df['pickup_datetime']

        UDP_IP = self._ip
        UDP_PORT = self._port
        print "UDP target IP:", UDP_IP
        print "UDP target port:", self._port



        sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP

        for i in range(0, len(df) - 1):
            date = df.ix[i]
            print(date)
            date_1 = df.ix[i][3]
            date_2 = df.ix[i + 1][3]
            diff = ((pd.to_datetime(date_2) - pd.to_datetime(date_1))).seconds * self._speedMultiplier
            MESSAGE = str(df.ix[i])
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            time.sleep(diff)
        sock.close()
        print ("Streamer closed")
        return