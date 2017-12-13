import csv
groupLines  = 100000

f = open('mockCSVData.csv','w')

f.write("accX,accY,accZ,rotA,rotB,rotC,magX,magY,magZ,timestamp" + "\n") 

for x in range(1, groupLines+1):
    f.write("0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0," + str(x*10) + "\n")  

#for x in range(groupLines+1, groupLines*2+1):
#    f.write("0.0,0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0," + str(x*10) + "\n")   
#
#for x in range(groupLines*2+1, groupLines*3+1):
#    f.write("0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.0,0.0," + str(x*10) + "\n")

f.close()
