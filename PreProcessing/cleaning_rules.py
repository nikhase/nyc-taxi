import pandas as pd
import numpy as np

event = pd.read_csv('/Users/Schlendrikovic/Documents/PyCharm_git/nyc-taxi/Tools/streamer/yellow_tripdata_2013-01.csv', nrows = 1)
event['pickup_datetime'] =pd.to_datetime(event['pickup_datetime'], format = '%Y-%m-%d %H:%M:%S')
event['dropoff_datetime'] =pd.to_datetime(event['dropoff_datetime'], format = '%Y-%m-%d %H:%M:%S')


# Zum testen
#event["dropoff_latitude"] = event["dropoff_latitude"].replace(40.751173 , np.nan)


#@Lars : Ab hier kannst du Sie benutzen .
flag = bool(True)
list = ["pickup_datetime" , "dropoff_datetime" , "trip_distance" , "pickup_longitude" , "pickup_latitude", "dropoff_longitude" ,  "dropoff_latitude" ]
event = event.replace(np.float64(0), np.nan)

for x in list:
    if event[x].isnull().any() or event[x].empty or event[x].ix[0] == 0 :
        flag = bool(False)
print flag


