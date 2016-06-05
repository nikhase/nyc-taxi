from Components import GraphHandler, Refresher, Reader
from threading import Thread


class RealtimeDB(object):

    def __init__(self, root, startIndex=0, rows=1000, speed=1, cacheSize=30):
        #Config
        self.root = root
        self.startIndex = startIndex
        self.rows = rows
        self.speed = speed
        self.cacheSize = cacheSize

        #Start
        self.run()

    def run(self):
        print "Started Realtime DB"
        #Start Reader and Refresher
        reader = Reader(self.root, startIndex=self.startIndex, rows=self.rows, speed=self.speed)
        r = Refresher(sleep=60)
        GraphHandler((reader, r), cache_size=self.cacheSize, speed=self.speed)
