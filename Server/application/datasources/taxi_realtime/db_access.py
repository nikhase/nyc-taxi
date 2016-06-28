from rdflib import Graph, URIRef
import rdflib.plugins.sparql.results.jsonlayer as jl
import json
import geotool as gt
import datetime as dt
import psycopg2


def getData(coordinates, radius, online=True):
    conn = psycopg2.connect("host='127.0.0.1' dbname='realtime_sql' user='raccess' password='read'")
    cur = conn.cursor()

    radius = 0.2

    for i in range(8):
        sqlStr = duration(coordinates['start_lat'], coordinates['start_lon'], coordinates['dest_lat'],
                          coordinates['dest_lon'], radius)
        cur.execute(sqlStr)
        rows = cur.fetchall()

        if len(rows) >= 1:
            #print "Radius: " + str(radius)
            break
        else:
            radius += 0.1

    conn.commit()
    conn.close()

    dictResults = []
    for result in rows:
        res = {}
        res['duration'] = str(result[5])
        res['start_lat'] = str(result[1])
        res['start_long'] = str(result[2])
        res['dest_lat'] = str(result[3])
        res['dest_long'] = str(result[4])
        dictResults.append(res)

    return json.dumps(dictResults)


def duration(originLat, originLong, destLat, destLong, radius=100):
    # Set the Query
    query = "SELECT * FROM public.events WHERE "
    # print query
    bounds = gt.boundingBox(originLat, originLong, radius)
    query += "events.pickup_latitude >=" + str(bounds[0]) + " AND "
    query += "events.pickup_latitude <=" + str(bounds[2]) + " AND "
    query += "events.pickup_longitude >=" + str(bounds[1]) + " AND "
    query += "events.pickup_longitude <=" + str(bounds[3]) + " AND "

    bounds = gt.boundingBox(destLat, destLong, radius)
    query += "events.dropoff_latitude >=" + str(bounds[0]) + " AND "
    query += "events.dropoff_latitude <=" + str(bounds[2]) + " AND "
    query += "events.dropoff_longitude >=" + str(bounds[1]) + " AND "
    query += "events.dropoff_longitude <=" + str(bounds[3]) + ";"

    return query
