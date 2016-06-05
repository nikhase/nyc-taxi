from Components import Listener, GraphHandler, Refresher, Reader


root="/Users/larshelin/Documents/Studium/Master/Semester 3/Seminar/Data/oneweekfrom20130107.csv"

#b = Listener(IP="127.0.0.1", Port=5005)
reader = Reader(root, startIndex=56975, rows=10000, speed=2)
r = Refresher(sleep=60)
graph = GraphHandler((reader, r), cache_size=30, speed=2)

while True:
    pass