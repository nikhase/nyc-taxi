import urllib, json

def getNeighborhood(lat, long):
    url = "http://api.geonames.org/neighbourhoodJSON?lat=" + str(lat) + "&lng=" + str(long) + "&username=demo"
    try:
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data['neighbourhood']['name']
    except Exception:
        return "Service not available"

def getPOI(lat, long):
    url = "http://api.geonames.org/findNearbyPOIsOSMJSON?lat=" + str(lat) + "&lng=" + str(long) + "&username=demo"
    try:
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        for poi in data['poi']:
            if not (poi['name'] == ""):
                return(poi['name'])

        return "No POI found."
    except Exception:
        return "Service not available"