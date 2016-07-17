from Components import GraphHandler, Refresher, Reader
import psycopg2
import datetime as dt

class RealtimeDB(object):

    def __init__(self, root, startIndex=0, rows=1000, speed=1, cacheSize=30, reset=True):
        #Config
        self.root = root
        self.startIndex = startIndex
        self.rows = rows
        self.speed = speed
        self.cacheSize = cacheSize

        if reset:
            # Reset the Database
            self.resetdatabase()

        #Start

        self.run()

    def run(self):
        print "Started Realtime DB"
        #Start Reader and Refresher
        reader = Reader(self.root, startIndex=self.startIndex, rows=self.rows, speed=self.speed)
        r = Refresher(sleep=60)
        self.graph = GraphHandler((reader, r), cache_size=self.cacheSize, speed=self.speed)
        self.initTimestamp = dt.datetime.now()


    def resetdatabase(self):
        # Try to connect
        try:
            #config = "database='postgres' user='postgres' password='admin' host='127.0.0.1' port='5432'"
            conn = psycopg2.connect("host='127.0.0.1' dbname='realtime_sql' user='postgres' password='admin'")
            #conn = psycopg2.connect(config)
        except:
            print "I am unable to connect to the database."
            raise IOError

        # Get the cursor
        cur = conn.cursor()
        try:

            # Clear tables
            cur.execute("DELETE  FROM public.events ;")
            conn.commit()
            conn.close()
            print("Database has been reset.")

        except Exception as e:
            print "Could not DELETE"
            raise e
