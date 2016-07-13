import rdflib
import datetime
import psycopg2


#SPARQL
def durationSPARQL(originLat, originLong, destLat, destLong, radius=100):
    # Set the Query
    query = """
            PREFIX ssn: <https://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
            PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select ?dur ?orLat ?orLong ?destLat ?destLong
            WHERE{
            ?obs ssn:hasDuration ?dur.
            ?obs ssn:observationResult ?oRes.
            ?oRes ssn:hasValue ?ov.
            ?orLoc geo:lat ?orLat. ?orLoc geo:long ?orLong.
            ?ov ssn:hasStartLocation ?orLoc.
            ?ov ssn:hasEndLocation ?destLoc.
            ?destLoc geo:lat ?destLat.
            ?destLoc geo:long ?destLong. """

    # Filter Results
    boundsOrigin = gt.boundingBox(originLat, originLong, radius)
    query += "FILTER ( (?orLat >= " + str(boundsOrigin[0]) + ") && (?orLat <= " + str(boundsOrigin[2]) + ") "
    query += "&& (?orLong >= " + str(boundsOrigin[1]) + ") && (?orLong <= " + str(boundsOrigin[3]) + ") )"

    boundsDest = gt.boundingBox(destLat, destLong, radius)
    query += "FILTER ( (?destLat >= " + str(boundsDest[0]) + ") && (?destLat <= " + str(boundsDest[2]) + ") "
    query += "&& (?destLong >= " + str(boundsDest[1]) + ") && (?destLong <= " + str(boundsDest[3]) + ") )"

    query += "} "
    # print query
    return query

#SQL
def durationSQL(originLat, originLong, destLat, destLong, radius=100):
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


def getData(coordinates, radius):
    conn = psycopg2.connect("host='127.0.0.1' dbname='realtime_sql' user='raccess' password='read'")
    cur = conn.cursor()

    sqlStr = durationSQL(coordinates['start_lat'], coordinates['start_lon'], coordinates['dest_lat'], coordinates['dest_lon'], radius)
    cur.execute(sqlStr)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for r in rows:
        continue

# Testing the speed of the rdflib SPARQL Query
g = rdflib.Graph()

g.load("output2000.txt", format="turtle")


Coordinates = {}

# Define Start
Coordinates['start_lat'] = 40.751573
Coordinates['start_lon'] = -73.991857

# Define End
Coordinates['dest_lat'] = 40.770475
Coordinates['dest_lon'] = -73.879504

sqlTimes = []
sparqlTimes = []
print (str(g.__len__()/11))

# Test it 10 times
for i in range(10):
    start = datetime.datetime.now()
    query = durationSPARQL(Coordinates['start_lat'], Coordinates['start_lon'], Coordinates['dest_lat'], Coordinates['dest_lon'])
    res = g.query(query)
    #print (str(g.__len__()/11))
    for result in res:
        #print result
        continue

    elapsedTime = datetime.datetime.now() - start
    sparqlTimes.append(elapsedTime.total_seconds())
    #print elapsedTime
    print "SPARQL Time elapsed: " + str(elapsedTime)

    start1 = datetime.datetime.now()
    results = getData(Coordinates, 1)

    elapsedTime = datetime.datetime.now() - start1

    print "SQL Time elapsed: " + str(elapsedTime)
    sqlTimes.append(elapsedTime.total_seconds())


print  "SPARQL Average: " + str(sum(sparqlTimes) /10)
print  "SQL Average: " + str(sum(sqlTimes) /10)



with open("result2000.txt", "w") as text_file:
    text_file.writelines("n = 2000, Runs = 10 \n" )
    text_file.writelines("SPARQL Average: " + str(sum(sparqlTimes) /10) + " Seconds per Query \n")
    text_file.writelines("SQL Average: " + str(sum(sqlTimes) /10) + " Seconds per Query \n")