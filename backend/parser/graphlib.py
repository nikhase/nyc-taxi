from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD
import datetime
from dateutil import parser

global graph
graph = Graph();

global SSN
global GEO
global DUL

# SSN Namespace
SSN = Namespace('https://www.w3.org/2005/Incubator/ssn/ssnx/ssn#')

# Geo Namespace
GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

# DUL Namespace
DUL = Namespace('http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#')


def parseDataframe(dataframe):
    initGraph();


    for index, row in dataframe.iterrows():

        date = parser.parse(row['dropoff_datetime'])

        if(date.day == 10):
            addToGraph(row)
        elif(date.day == 20):
            continue
        elif(date.day > 10):
            break

    return graph;



def initGraph():
    # Bind Namespace to abbreviation
    graph.bind('ssn', SSN)
    graph.bind('geo', GEO)
    graph.bind('dul', DUL)
    return

def addToGraph(event):
    observation = BNode();

    oTime = BNode();
    # Observation
    graph.add((observation, RDF.type, SSN.Observation))
    graph.add((oTime, RDF.type, DUL.TimeInterval))
    graph.add((observation, SSN.observationSamplingTime, oTime))

    # Time
    t = Literal(event['dropoff_datetime'], datatype=XSD.dateTime)
    #t = Literal(event['dropoff_datetime'])
    #print(event['dropoff_datetime'])
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
    dur  = parser.parse(event['dropoff_datetime']) - parser.parse(event['pickup_datetime'])
    duration = Literal(str(dur), datatype=XSD.float)

    graph.add( (observation, SSN.hasDuration, duration))

    return
