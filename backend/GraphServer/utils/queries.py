import datetime
import geotool as gt

def getDuration():
    query = """
        PREFIX ssn: <https://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
        PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?duration
        WHERE {
            ?obs  ssn:hasDuration ?duration .
            } LIMIT 10
            """
    return query

def duration(originLat, originLong, destLat, destLong, radius=100):
        #Set the Query
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

        #Filter Results
        boundsOrigin = gt.boundingBox(originLat, originLong, radius)
        query += "FILTER ( (?orLat >= " + str(boundsOrigin[0]) + ") && (?orLat <= " + str(boundsOrigin[2]) + ") "
        query += "&& (?orLong >= " + str(boundsOrigin[1]) + ") && (?orLong <= " + str(boundsOrigin[3]) + ") )"

        boundsDest = gt.boundingBox(destLat, destLong, radius)
        query += "FILTER ( (?destLat >= " + str(boundsDest[0]) + ") && (?destLat <= " + str(boundsDest[2]) + ") "
        query += "&& (?destLong >= " + str(boundsDest[1]) + ") && (?destLong <= " + str(boundsDest[3]) + ") )"

        query += "} LIMIT 100"
        #print query
        return query



def getEvents(timestamp):

    query = """
        PREFIX ssn: <https://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
        PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?obs ?oRes ?ov ?start ?end ?obsTime
        WHERE {
            ?obs  rdf:type ?y.
            ?obs ssn:observationResult ?oRes.
            ?oRes rdf:type ?sensorOutput.
            ?oRes ssn:hasValue ?ov.
            ?ov ssn:hasStartLocation ?start.
            ?ov ssn:hasEndLocation ?end.
            ?obs  ssn:observationSamplingTime ?obsTime .
            ?obsTime dul:hasRegionDataValue ?date.
            """
    query += "FILTER ( ?date <\"" + timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "\"^^xsd:dateTime )}"
    return query

def testQuery():
    query = """
        PREFIX ssn: <https://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
        PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT *
        WHERE {
            ?obs  rdf:type ?y.
    }"""
    return query