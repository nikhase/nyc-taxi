from rdflib import Graph, URIRef
import utils.queries as query
import json
import copy

update = True;

#Connecting to DB
configString= ("dbname=postgres user=raccess password=read")
g = Graph('PostgreSQL', identifier=URIRef("http://example.com/g1"))
g.open(configString, create=False)

#g = copy.deepcopy(graph)



#Define Start
StartLat= 40.751573
StartLon= -73.991857

#Define End
DestLat = 40.770475
DestLon = -73.879504




if update:
    print "Update"
    results = g.query("SELECT * WHERE {?s ?p ?o.}")
    print len(results)
    for result in results:
        for node in result:
            g.remove((node, None, None))
    print str(g.__len__()/11)
    #g = Graph()
    g.commit()

else:
    print "Query"
    #results = g.query(query.testQuery())
    results = g.query(query.duration(StartLat, StartLon, DestLat, DestLon, 1))

    dictResults = []
    for result in results:
        res = {}
        res['duration'] = str(result[0])
        res['start_lat'] = str(result[1])
        res['start_long'] = str(result[2])
        res['dest_lat'] = str(result[3])
        res['dest_long'] = str(result[4])
        dictResults.append(res)
        print str(result[1]) + ", " + str(result[2])
        print str(result[3]) + ", " + str(result[4])
    print json.dumps(dictResults)

print ("Number of events: " + str(g.__len__()/11))
#print (g.serialize(format="turtle"))

g.close()