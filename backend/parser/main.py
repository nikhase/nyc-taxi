import pandas as pd
import graphlib as gl
import time
import os as os

path="/Users/larshelin/Documents/Studium/Master/Semester 3/Seminar/Data/oneweekfrom20130107.csv"

df =pd.read_csv(path, nrows=2000)

#df = pd.read_csv('trips_shortend.csv')
#print(df.columns.values)

#graph = gl.parseEvent(df.ix[0]);

print("Start Parsing")
start = time.time()
graph = gl.parseDataframe(df)

end = time.time()
elapsed = end-start
perEvent = elapsed / len(df)
print(perEvent)

graph.serialize(destination='output2000.txt', format='turtle')

