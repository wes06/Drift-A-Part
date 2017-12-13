import csv
from collections import defaultdict


with open('../mockCSVGenerator-rdmUnsigned/mockCSVData.csv', newline='') as csvfile:
	IMUData = csv.DictReader(csvfile) # read rows into a dictionary format
	#print("Fieldnames are " + str(IMUData.fieldnames))
	#print("\n")

	#starting vars
	velX = 0
	posX = 0
	previousAccX = 0
	velY = 0
	posY = 0
	previousAccY = 0
	velZ = 0
	posZ = 0
	previousAccZ = 0

	previousTimestamp = 0
	dataPointCt = 0


	for row in IMUData:

		# deltaT = (current timestap - last timestamp)
		# divided by 1000 to convert from millis to seconds
		deltaT = float((int(row['timestamp']) - previousTimestamp))/1000

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

		# save the timestant to calculate next deltaT
		previousTimestamp = int(row['timestamp'])

		dataPointCt += 1


avgVelX = posX/(previousTimestamp/1000)
avgVelY = posY/(previousTimestamp/1000)
avgVelZ = posZ/(previousTimestamp/1000)

print('Integrated %i data points.\n' % dataPointCt)


print('X\tFinal speed:\t\t %.2f m/s' % velX)
print('\tFinal position:\t\t %.2f m' % posX)
print('\tAverage speed:\t\t %.2f m/s' % avgVelX)

print('\nY\tFinal speed:\t\t %.2f m/s' % velY)
print('\tFinal position:\t\t %.2f m' % posY)
print('\tAverage speed:\t\t %.2f m/s' % avgVelY)

print('\nZ\tFinal speed:\t\t %.2f m/s' % velZ)
print('\tFinal position:\t\t %.2f m' % posZ)
print('\tAverage speed:\t\t %.2f m/s \n' % avgVelZ)

