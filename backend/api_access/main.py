import pandas as pd
import geonames as gn

#Enter csv path
path = "/Users/larshelin/Documents/PycharmProjects/CEP/nyc-taxi/backend/parser/trips_shortend.csv"

#Open Dataframe
df = pd.read_csv(path)

for i in range(0,10):
    # Get Latitude and Longitude
    lat = df.ix[i]['pickup_latitude']
    long = df.ix[i]['pickup_longitude']
    print(gn.getNeighborhood(lat,long))
    print(gn.getPOI(lat, long))