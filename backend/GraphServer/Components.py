from threading import Thread
from socket import *
import time
import rdflib as rdf
import json
import utils.graphlib as gl
import datetime as dt


class GraphHandler:
    def __init__(self, observable, basetime = dt.datetime.now() ,cache_size=30):
        self.g = rdf.Graph()
        self.buffer = rdf.Graph()
        self.cache_size = cache_size
        self.refTime = dt.datetime.now()
        self.baseTime = basetime;
        self.buffering = False;
        observable.register_observer(self)

    def addObservable(self, observable):
        observable.register_observer(self)

    def notify(self,observer, arg, action):
        if action == "add":
            if self.buffering:
                self.__addDataBuffer(arg)
            else:
                self.__addData(arg)

        elif action == "refresh":
            self.__refresh()


    def __refresh(self):
        elapsed = dt.datetime.now() - self.refTime
        artNow = self.baseTime + elapsed
        threshold = artNow - dt.timedelta(minutes=self.cache_size)
        gl.removeFromGraph(threshold, self.g)


    def __addData(self, arg):
        data = json.loads(arg)
        self.g = self.g + (gl.addToGraph(data, self.g))

    def __addDataBuffer(self, arg):
        data = json.loads(arg)
        self.buffer = self.buffer + (gl.addToGraph(data, self.buffer))

    def lock(self):
        self.buffer = rdf.Graph()
        self.buffering = True

    def unlock(self):
        self.buffering = False
        self.g = self.g + self.buffer
        print ("Buffered " + str(self.buffer.__len__()))
        self.buffer = rdf.Graph()

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
            except socket.error, e:
                print ("Listener: Error Receivng Data")
            except IOError:
                print ("Listener: IO Error")


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