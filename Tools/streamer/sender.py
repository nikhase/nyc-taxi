import socket
import pandas as pd
import time

df = pd.read_csv("/Users/Schlendrikovic/Documents/Uni/SS 2016/EventProcessing/Daten/oneweekfrom20130107.csv");

# drop unnecessary columns
df.drop(
    ['Unnamed: 0', 'hack_license', 'payment_type', 'pfare_amount', 'surcharge', 'tip_amount', 'total_amount',
     'passenger_count', 'medallion'], axis=1, inplace=1)
# print(df.head())

# Datetime right Format
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')

# sort by pickup_datetime
df.sort_values("pickup_datetime")
df.index = df['pickup_datetime']

UDP_IP = "127.0.0.1"
UDP_PORT = 5005


print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:",

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

for i in range(0,len(df)-1):
    date = df.ix[i]
    print(date)
    date_1 = df.ix[i][0]
    date_2 = df.ix[i + 1][0]
    diff = (pd.to_datetime(date_2) - pd.to_datetime(date_1)).seconds
    MESSAGE = str(df.ix[i])
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(diff)


sock.close()