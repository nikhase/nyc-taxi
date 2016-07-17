import pandas as pd
import datetime 
import time

#Status
print("Read File")

#Load the data file (here only a few columns)
df = pd.read_csv('trips_shortend.csv', usecols=[1,4,5,6,15])

#Convert to datetime
df['pickup_datetime'] =pd.to_datetime(df['pickup_datetime'])

#Sort the Dataframe
df.sort_values('pickup_datetime', inplace=True)

#Re-Indexing the data set. This way we can access it via df.ix[i] and df.ix[i+1]
df.index = range(0,len(df))


#Iterate data (20 elements)
for i in range(0,20):
	#Get the i-th and i+1-th datetime
	date_t0 = df.ix[i][0]
	date_t1 = df.ix[i+1][0]

	#Calculate difference between current and the next event
	diff = (pd.to_datetime(date_t1) - pd.to_datetime(date_t0)).seconds

	#wait until next event occuts
	#time.sleep(diff)

    #Print the data
    print(str(df.ix[i+1]))




print("Done")