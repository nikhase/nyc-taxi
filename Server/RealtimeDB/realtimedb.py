from Components import GraphHandler, Refresher, Reader
import psycopg2

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
        GraphHandler((reader, r), cache_size=self.cacheSize, speed=self.speed)

    def resetdatabase(self):
        # Try to connect
        try:
            #config = "database='postgres' user='postgres' password='admin' host='127.0.0.1' port='5432'"
            conn = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='admin'")
            #conn = psycopg2.connect(config)
        except:
            print "I am unable to connect to the database."
            raise IOError

        # Get the cursor
        cur = conn.cursor()
        try:

            # Clear tables
            cur.execute("DELETE  FROM public.kb_bec6803d52_asserted_statements;")
            cur.execute("DELETE  FROM public.kb_bec6803d52_literal_statements;")
            cur.execute("DELETE  FROM public.kb_bec6803d52_namespace_binds;")
            cur.execute("DELETE  FROM public.kb_bec6803d52_quoted_statements;")
            cur.execute("DELETE  FROM public.kb_bec6803d52_type_statements;")

            conn.commit()
            conn.close()
            print("Database has been reset.")

        except Exception as e:
            print "Could not DELETE"
            raise e
