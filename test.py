from queue import Queue
from collections import deque

q= Queue(10)

a= [['a','b'],['c','d']]
b= [['e','f'],['g','h']]

for item in a:
    q.put(item)
for item in b:
    q.put(item)

while not q.empty():
    print(q.get()[1])