from rdflib import Graph


def search(args):

    result = {  "seconds": 600 , "accuracy" : 0.72}

    g = Graph()
    g.parse("data.ttl", format='n3')
    qres = g.query(
        """
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        SELECT DISTINCT ?b
           WHERE {
              ?a geo:lat ?b .
           }""")

    print(len(qres))
    for row in qres:
        print(str(row))

    return result



search("hi")