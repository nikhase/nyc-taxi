import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('99_2100_distance.csv')



print(len(df))

df['circuity'] = df['real'] / df['euclidian']

#df.
print df.head()
print df['circuity'].describe()

#print df.loc[df['circuity'].idxmax()]

# Remove equal timestamps
df = df[(df.start_timestamp != df.dest_timestamp)]

df = df[(df.start_lon != df.dest_lon) & (df.start_lat != df.dest_lat)]
df = df[df.euclidian > 10]

df = df[df['circuity'] >= 1]


print df['circuity'].describe()

with open("circuity.txt", 'wb') as file:
    file.write(str(df['circuity'].describe()))


#plt.pyplot.style.use = 'default'
#df['circuity'].plot.box()
#plt.show()
#factors = []

