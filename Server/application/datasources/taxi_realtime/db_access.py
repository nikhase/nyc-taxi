from rdflib import Graph, URIRef
import rdflib.plugins.sparql.results.jsonlayer as jl
import json
import geotool as gt
import datetime as dt


def getData(coordinates, radius, online=True):
    # Using the online Flag to load either a local file or use a DB

    #Connecting to DB
    if online:
        t1 = dt.datetime.now()
        configString = "dbname=postgres user=raccess password=read"
        g = Graph('PostgreSQL', identifier=URIRef("http://example.com/g1"))
        g.open(configString, create=False)
        print "Getting the graph took: " + str((dt.datetime.now() - t1).seconds)
    else:
        path = "/Users/larshelin/Documents/PycharmProjects/CEP/nyc-taxi/Server/application/datasources/taxi_realtime/output.txt"
        print str(path)
        g = Graph()
        g.load(str(path), format="turtle")
        print str(g.__len__() / 11)


    print "Traversing the graph (size: " + str(g.__len__()) + ")"

    results = g.query(duration(coordinates['start_lat'], coordinates['start_lon'], coordinates['dest_lat'], coordinates['dest_lon'], radius))
    t1 = dt.datetime.now()
    dictResults = []
    for result in results:
        res = {}
        res['duration'] = str(result[0])
        res['start_lat'] = str(result[1])
        res['start_long'] = str(result[2])
        res['dest_lat'] = str(result[3])
        res['dest_long'] = str(result[4])
        dictResults.append(res)

    print "Traversing took: " + str((dt.datetime.now() - t1).seconds)
    g.close()
    return json.dumps(dictResults)


def duration(originLat, originLong, destLat, destLong, radius=100):
    # Set the Query
    query = """
            PREFIX ssn: <https://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
            PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select distinct ?dur ?orLat ?orLong ?destLat ?destLong
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

    query += "} LIMIT 10"
    # print query
    return query