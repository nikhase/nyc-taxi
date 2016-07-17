import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df1 = pd.read_csv('2000_4500.csv')

df2 = pd.read_csv('5000_8000.csv')
df3 = pd.read_csv('8000_10000.csv')
df4 = pd.read_csv('100_2100.csv')

"""df = df1
df.append(df2 , ignore_index=True)
df.append(df3, ignore_index=True)
df.append(df4, ignore_index=True)"""
frames = [df1, df2, df3,df4]

df = pd.concat(frames)


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

with open("circuity4.txt", 'wb') as file:
    file.write(str(df['circuity'].describe()))


#plt.pyplot.style.use = 'default'
df['circuity'].plot.box()
#plt.hist(df['circuity'], bins=20)
plt.show()
#factors = []

