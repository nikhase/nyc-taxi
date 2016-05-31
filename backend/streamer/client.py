import streamer as streamerbsp
import listener as listenerbsp
import time
import pandas as pd

#
root="/Users/larshelin/Documents/Studium/Master/Semester 3/Seminar/Data/oneweekfrom20130107.csv"
ip="127.0.0.1"
speed=0.1

#lt_1 = time.strftime("%d.%m.%Y %H:%M:%S")
#print lt_1
#lt_1=pd.to_datetime(lt_1)


#listener_ref = listenerbsp.listener(ip,5005)
streamer_ref = streamerbsp.streamer(ip,5005,root)
streamer_ref.start(speed)
#listener_ref.start

#lt_2 = time.strftime("%d.%m.%Y %H:%M:%S")
#print lt_2
#lt_2 = pd.to_datetime(lt_2)

#diff= (lt_2 - lt_1).seconds
#print 'Streamer Arbeitszeit  = ' , diff , " Sekunden"