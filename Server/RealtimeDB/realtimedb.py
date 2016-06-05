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
            conn = psycopg2.connect("dbname='postgres' user='postgres' password='admin'")
        except:
            print "I am unable to connect to the database."

        # Get the cursor
        cur = conn.cursor()
        try:

            # Clear tables
            cur.execute("""DELETE  FROM public.kb_bec6803d52_asserted_statements;""")
            cur.execute("""DELETE  FROM public.kb_bec6803d52_literal_statements;""")
            cur.execute("""DELETE  FROM public.kb_bec6803d52_namespace_binds;""")
            cur.execute("""DELETE  FROM public.kb_bec6803d52_quoted_statements;""")
            cur.execute("""DELETE  FROM public.kb_bec6803d52_type_statements;""")

            print("Database has been reset.")
        except Exception:
            print "Could not DELETE"
