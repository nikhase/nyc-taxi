from dateutil import parser
from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, URIRef

import queries

global SSN
global GEO
global DUL

# SSN Namespace
SSN = Namespace('https://www.w3.org/2005/Incubator/ssn/ssnx/ssn#')

# Geo Namespace
GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

# DUL Namespace
DUL = Namespace('http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#')

def addToGraph(event, graphURI = "http://example.com/g1", db_conf={"dbname" : "postgres", "user" : "postgres", "password" : "admin" }):
    #configString = ("dbname=postgres user=waccess password=write")
    configString = ("dbname=" + db_conf['dbname'] + " user="+ db_conf['user'] + " password=" + db_conf['password'])
    #print configString
    graph = Graph('PostgreSQL', identifier=URIRef(graphURI))

    graph.open(configString, create=False)

    graph.bind('ssn', SSN)
    graph.bind('geo', GEO)
    graph.bind('dul', DUL)
    observation = BNode();

    oTime = BNode();

    # Observation
    graph.add((observation, RDF.type, SSN.Observation))
    graph.add((oTime, RDF.type, DUL.TimeInterval))
    graph.add((observation, SSN.observationSamplingTime, oTime))

    # Time
    date = parser.parse(event['pickup_datetime'])
    t = Literal(date.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)
    graph.add((oTime, DUL.hasRegionDataValue, t))

    # SensorOutput
    sensorOutput = BNode();

    graph.add((sensorOutput, RDF.type, SSN.SensorOutput))
    graph.add((observation, SSN.observationResult, sensorOutput))

    # ObservationValue
    observationValue = BNode()
    startLocation = BNode()
    endLocation = BNode()
    graph.add((observationValue, RDF.type, SSN.ObservationValue))
    graph.add((sensorOutput, SSN.hasValue, observationValue))

    # Start and End Location
    graph.add((observationValue, SSN.hasStartLocation, startLocation))
    graph.add((observationValue, SSN.hasEndLocation, endLocation))
    graph.add((startLocation, RDF.type, GEO.location))
    graph.add((endLocation, RDF.type, GEO.location))

    # Start Location
    lat = Literal(event['pickup_latitude'], datatype=XSD.float)
    long = Literal(event['pickup_longitude'], datatype=XSD.float)

    # Adding the start location
    graph.add((startLocation, GEO.lat, lat))
    graph.add((startLocation, GEO.long, long))

    # End Location
    lat = Literal(event['dropoff_latitude'], datatype=XSD.float)
    long = Literal(event['dropoff_longitude'], datatype=XSD.float)

    # Adding the start location
    graph.add((endLocation, GEO.lat, lat))
    graph.add((endLocation, GEO.long, long))

    #Duration
    date1 = parser.parse(event['dropoff_datetime'])
    date2 = parser.parse(event['pickup_datetime'])
    dur = date1 - date2
    duration = Literal(str(dur), datatype=XSD.float)

    graph.add((observation, SSN.hasDuration, duration))

    #print str(graph.__len__() / 11)
    #Commit and close the graph
    graph.commit()
    graph.close()


def removeFromGraph(timestamp, graphURI = "http://example.com/g1", db_conf={"dbname" : "postgres", "user" : "postgres", "password" : "admin" }):
    configString = ("dbname=postgres user=waccess password=write")
    #configString = ("dbname=" + db_conf['dbname'] + "user="+ db_conf['user'] + " password=" + db_conf['password'])
    graph = Graph('PostgreSQL', identifier=URIRef(graphURI))
    graph.open(configString, create=False)
    results = graph.query(queries.getEvents(timestamp))

    print len(results)
    for result in results:
        for node in result:
            graph.remove((node, None, None))

    # Commit and close the graph
    graph.commit()
    graph.close()
