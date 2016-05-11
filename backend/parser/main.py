import pandas as pd
import graphlib as gl
import time
import os as os

path = os.path.expanduser("~/Documents/Studium/Master/Semester 3/Seminar/Data/yellow_tripdata_2014-01.csv")

#df = pd.read_csv('trips_shortend.csv')
df = pd.read_csv(path)
#print(df.columns.values)

#graph = gl.parseEvent(df.ix[0]);

print("Start Parsing")
start = time.time()
graph = gl.parseDataframe(df)

end = time.time()
elapsed = end-start
perEvent = elapsed / len(df)
print(perEvent)

graph.serialize(destination='output.txt', format='turtle')

