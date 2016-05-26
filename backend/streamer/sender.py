import socket
import pandas as pd
import time

df = pd.read_csv("trips_shortend.csv", nrows=10);

UDP_IP = "127.0.0.1"
UDP_PORT = 5005


print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:",

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

for i in range(0,9):
    MESSAGE = str(df.ix[i])

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(3)