import csv
import math
import time

from collections import defaultdict

from os import path

dir = path.dirname(__file__)


timestr = time.strftime("%Y%m%d-%H%M%S")

with open('refPos.csv', 'w') as out_csvreffile:
	# columns for output CSV file
	fieldnames = ['refPosX', 'refPosY', 'refPosZ']

	# initialize writer
	refPosData = csv.DictWriter(out_csvreffile, fieldnames=fieldnames)

	for x in range(-2,2):
		refPos = pow(10,(x*3))
		print('pos: %.6f,' % refPos)
		logPos = math.log10(abs(refPos*10000))
		print('log pos: %.6f,' % logPos)
			# output info to CSV
		refPosData.writerow({
			'refPosX': '%0.6f' % logPos,
			'refPosY': '%0.6f' % logPos,
			'refPosZ': '%0.6f' % logPos
			})
	


with open(path.join(dir, "..","..","datalogs","20180115-16h57m.CSV"), newline='') as in_csvfile, open('output/positions-log10-{}.csv'.format(timestr), 'w') as out_csvfile:
	
	# columns for output CSV file
	fieldnames = ['posX', 'posY', 'posZ']

	# initialize writer
	posData = csv.DictWriter(out_csvfile, fieldnames=fieldnames)

	# write column names to output CSV file
	#posData.writeheader()

	# read rows into a dictionary format
	IMUData = csv.DictReader(in_csvfile) 

	# I/O fieldnames
	print("Input fieldnames are " + str(IMUData.fieldnames))
	print("Output fieldnames are " + str(posData.fieldnames))
	print("\n")

	#starting vars
	velX = 0
	posX = 0
	distX = 0
	previousAccX = 0
	velY = 0
	posY = 0
	distY = 0
	previousAccY = 0
	velZ = 0
	posZ = 0
	distZ = 0
	previousAccZ = 0

	logPosX = 0
	logPosY = 0
	logPosZ = 0

	previousTimestamp = 0
	dataPointCt = 0

	print("GO!\n\n")

	for row in IMUData:

		# deltaT = (current timestap - last timestamp)
		# divided by 1000 to convert from millis to seconds
		deltaT = float(row['timestamp'])/1000
		#float((int(row['timestamp']) - previousTimestamp))/10

		# deltaVelX: gained velocity
		# integration of acceleration over time
		# acceleration of the period considered average of current instantaneous acc and previous
		deltaVelX = (previousAccX + (float(row['accX'])-previousAccX)/2) * deltaT 
		previousAccX = float(row['accX'])
		deltaVelY = (previousAccY + (float(row['accY'])-previousAccY)/2) * deltaT 
		previousAccY = float(row['accY'])
		deltaVelZ = (previousAccZ + (float(row['accZ'])-previousAccZ)/2) * deltaT 
		previousAccZ = float(row['accZ'])

		# new speed after integrated acceleration
		velX += deltaVelX
		velY += deltaVelY
		velZ += deltaVelZ

		# pos: last position + integration of speed over time
		posX += velX * deltaT
		posY += velY * deltaT
		posZ += velZ * deltaT

		# dist: total elapsed distance
		# i.e. moving forward 1m and back 1m counts as 2m
		distX += abs(velX * deltaT)
		distY += abs(velY * deltaT)
		distZ += abs(velZ * deltaT)

		# save the timestant to calculate next deltaT
		previousTimestamp = row['timestamp']

		# add a read datapoint to counter
		dataPointCt += 1
		
		print('posX: %.6f,\tposY: %.6f,\tposZ: %.6f,\tdT: %.3f' % (posX, posY, posZ, deltaT))

		if posX < 0:
			logPosX = math.log10(abs(posX*10000)) * (-1)
		else:
			logPosX = math.log10(abs(posX*10000))

		if posY < 0:
			logPosY = math.log10(abs(posY*10000)) * (-1)
		else:
			logPosY = math.log10(abs(posY*10000))

		if posZ < 0:
			logPosZ = math.log10(abs(posZ*10000)) * (-1)
		else:
			logPosZ = math.log10(abs(posZ*10000))

		if dataPointCt < 10000:
			
			# output info to CSV
			posData.writerow({
				'posX': '%0.6f' % logPosX,
				'posY': '%0.6f' % logPosY,
				'posZ': '%0.6f' % logPosZ
				})
		else:
			break


# average speed calculation, assumes first timestamp = 0
avgVelX = posX/100#(previousTimestamp/1000)
avgVelY = posY/100#(previousTimestamp/1000)
avgVelZ = posZ/100#(previousTimestamp/1000)


print('Integrated %i data points.\n' % dataPointCt)

print('X\tFinal speed:\t\t %.2f m/s' % velX)
print('\tFinal position:\t\t %.2f m' % posX)
print('\tAverage speed:\t\t %.2f m/s' % avgVelX)
print('\tElapsed distance:\t %.2f m' % distX)

print('\nY\tFinal speed:\t\t %.2f m/s' % velY)
print('\tFinal position:\t\t %.2f m' % posY)
print('\tAverage speed:\t\t %.2f m/s' % avgVelY)
print('\tElapsed distance:\t %.2f m' % distY)

print('\nZ\tFinal speed:\t\t %.2f m/s' % velZ)
print('\tFinal position:\t\t %.2f m' % posZ)
print('\tAverage speed:\t\t %.2f m/s' % avgVelZ)
print('\tElapsed distance:\t %.2f m\n' % distZ)

