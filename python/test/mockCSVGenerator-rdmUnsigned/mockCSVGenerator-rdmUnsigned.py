import csv
import random

groupLines  = 300000

f = open('mockCSVData.csv','w')

f.write("accX,accY,accZ,rotA,rotB,rotC,magX,magY,magZ,timestamp" + "\n") 

for x in range(1, groupLines+1):
	rdmX = random.uniform(-0.01, 0.01)
	rdmY = random.uniform(-0.01, 0.01)
	rdmZ = random.uniform(-0.01, 0.01)
	f.write("%.8f,%.8f,%.8f,0.0,0.0,0.0,0.0,0.0,0.0,%i\n" % (rdmX, rdmY, rdmZ, x*10))  

f.close()
