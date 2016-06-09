from dateutil import parser
import psycopg2

def addData(event):
    conn = psycopg2.connect("host='127.0.0.1' dbname='realtime_sql' user='postgres' password='admin'")
    cur = conn.cursor()

    # Time
    date = event['pickup_datetime']
    #t = date.strftime("%Y-%m-%dT%H:%M:%S")


    # Start Location
    lata = event['pickup_latitude']
    longa = event['pickup_longitude']

    # End Location
    latb = event['dropoff_latitude']
    longb = event['dropoff_longitude']


    #Duration
    date1 = parser.parse(event['dropoff_datetime'])
    date2 = parser.parse(event['pickup_datetime'])
    dur = date1 - date2
    cur.execute("INSERT INTO public.events VALUES (TIMESTAMP \'" + str(date) + "\', " + str(lata) + ", " + str(longa) + ", " + str(latb) + ", " + str(longb) + ", " + str(dur.seconds) + ");" )

    conn.commit()
    conn.close()

def removeDate(timestamp):
    conn = psycopg2.connect("host='127.0.0.1' dbname='realtime_sql' user='postgres' password='admin'")
    cur = conn.cursor()

    formTimestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S");
    sqlStr = "DELETE FROM public.events " \
             "WHERE timestamp < to_timestamp(\'" + formTimestamp+ "\', \'YYYY-MM-DD HH24:MI:SS\') ;"
    print sqlStr
    cur.execute(sqlStr)

    conn.commit()
    conn.close()