from threading import Thread
from socket import *
import time
import json
import utils.postgresInterface as post
import datetime as dt
import dateutil
import pandas as pd

class GraphHandler:
    def __init__(self, observables ,cache_size=30, speed=1):
        self.cache_size = cache_size
        self.refTime = dt.datetime.now()
        self.baseTime = dt.datetime.now()
        self.__speed = speed
        self.__initialized = False
        for observable in observables:
            observable.register_observer(self)

    def addObservable(self, observable):
        observable.register_observer(self)

    def notify(self,observer, arg, action):
        if action == "add":
            self.__addData(arg)
        elif action == "refresh":
            self.__refresh()


    def __refresh(self):
        elapsed = dt.datetime.now() - self.refTime
        artNow = self.baseTime + elapsed * self.__speed
        threshold = artNow - dt.timedelta(minutes=self.cache_size)
        print artNow
        print("Delete all before: " + str(threshold))
        post.removeDate(threshold)


    def __addData(self, arg):
        data = json.loads(arg)
        if not self.__initialized:
            self.__initialize(data)
            self.__initialized = True

            print "Basetime initialized to " + str(self.baseTime)
        post.addData(data)

    def __initialize(self, data):
        date = dateutil.parser.parse(data['pickup_datetime'])
        self.baseTime = date
        print str(self.baseTime)
        #self.baseTime = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


class Listener(Thread):

    def __init__(self, IP, Port):
        self.UDP_IP = IP
        self.UDP_Port = Port
        self.sock = socket()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.UDP_IP, self.UDP_Port))
        self.__observers = []
        Thread.__init__(self)

        self.daemon = True
        self.start()


    def run(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
                self.notify_observers(data, action="add")
            except IOError:
                print ("Listener: IO Error")


    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, arg, action):
        for observer in self.__observers:
            observer.notify(self, arg, action)


class Reader(Thread):
    def __init__(self, path, startIndex=0, rows=1000, speed=1):
        #Set the speed multiplier
        self._speedMultiplier = float(1) / float(speed)

        #Set start index and rows to be used
        self.__I = startIndex
        self.__rows = rows
        totalRows = startIndex + rows

        #Read File, sort it
        self.__df = pd.read_csv(path, nrows=totalRows)
        self.__df['pickup_datetime'] = pd.to_datetime(self.__df['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
        self.__df['dropoff_datetime'] = pd.to_datetime(self.__df['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
        self.__df.sort_values("pickup_datetime")
        #self.__df.index = self.__df['pickup_datetime']
        #self.__df.index = range(0, len(self.__df))

        #Set up observer
        self.__observers = []
        Thread.__init__(self)

        #Start Thread
        self.daemon = True
        self.start()

    def run(self):
        print "Start reading file."
        print "Starting at: " + str(self.__I) + " to " + str(self.__I + self.__rows)

        for i in xrange(self.__I, self.__I + self.__rows - 1):
            date_1 = self.__df.ix[i]['pickup_datetime']
            date_2 = self.__df.ix[i + 1]['pickup_datetime']
            diff = (pd.to_datetime(date_2) - pd.to_datetime(date_1)).seconds * self._speedMultiplier
            msg = str(self.__df.ix[i].to_json(date_format="iso"))
            self.notify_observers(msg, action="add")
            #print diff
            time.sleep(diff)

        print "Done reading file."

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, arg, action):
        for observer in self.__observers:
            observer.notify(self, arg, action)

class Refresher(Thread):

    def __init__(self, sleep=60):
        self.sleep = sleep
        self.running = True
        self.__observers = []
        Thread.__init__(self)

        self.daemon = True
        self.start()

    def run(self):
        while self.running:
            time.sleep(self.sleep)
            self.notify_observers("", action="refresh")

    def refreshRate(self, sleep):
        self.sleep = sleep

    def stop(self):
        self.running = False

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, arg, action):
        for observer in self.__observers:
            observer.notify(self, arg, action)