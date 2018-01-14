import csv
from collections import defaultdict


with open('../mockCSVGenerator-rdmUnsigned/DATALOG4.CSV', newline='') as in_csvfile, open('positions.csv', 'w') as out_csvfile:
	
	# columns for output CSV file
	fieldnames = ['posX', 'posY', 'posZ']

	# initialize writer
	posData = csv.DictWriter(out_csvfile, fieldnames=fieldnames)

	# write column names to output CSV file
	posData.writeheader()

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
		previousTimestamp = int(row['timestamp'])

		# add a read datapoint to counter
		dataPointCt += 1
		
		# output info to CSV
		posData.writerow({
			'posX': '%0.6f' % posX,
			'posY': '%0.6f' % posY,
			'posZ': '%0.6f' % posZ
			})

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

