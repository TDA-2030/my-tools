# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

print(sys.argv[1])

def get_time():
    timestamp = []
    high = []
    low = []
    interval=[]
    i=0

    csv_reader = csv.reader(open(sys.argv[1]))
    for row in csv_reader:
        i=i+1
        if i>=10:
            timestamp.append(1000000*float(row[0]))
    
    for i in range(0, len(timestamp)):
        if i>=1:
            interval.append(timestamp[i]-timestamp[i-1])
            if i%2 ==0 :
                high.append(timestamp[i]-timestamp[i-1])
            else:
                low.append(timestamp[i]-timestamp[i-1])

    return interval, high, low

[time, h, l] = get_time()
print(len(time))

print("HIGH var=%f err=%f" % (np.var(h), np.max(h)-np.min(h)))
print("LOW var=%f err=%f" % (np.var(l), np.max(l)-np.min(l)))

x=range(0,len(time))
y=time

plt.figure(figsize=(10, 10), dpi=100)
plt.scatter(x,y,c = 'r',marker = '.')
plt.show()


