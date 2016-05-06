import pandas as pd
import graphlib as gl
import time


df = pd.read_csv('trips_shortend.csv')
#print(df.columns.values)

#graph = gl.parseEvent(df.ix[0]);

start = time.time()
graph = gl.parseDataframe(df)

end = time.time()
elapsed = end-start
perEvent = elapsed / len(df)
print(perEvent)
graph.serialize(destination='output.txt', format='turtle')

