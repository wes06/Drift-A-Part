import csv
from collections import defaultdict


with open('../mockCSVGenerator/mockCSVData.csv', newline='') as csvfile:
	IMUData = csv.DictReader(csvfile) # read rows into a dictionary format
	print("Fieldnames are " + str(IMUData.fieldnames))
	print("\n")

	#starting vars
	velX = 0
	distX = 0
	previousTimestamp = 0
	previousAccX = 0
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
		
		# new speed after integrated acceleration
		velX += deltaVelX

		# distX: last distance + integration of speed over time
		distX += velX * deltaT

		# save the timestant to calculate next deltaT
		previousTimestamp = int(row['timestamp'])

		dataPointCt += 1


avgVelX = distX/(previousTimestamp/1000)

print('Integrated %i data points.\n' % dataPointCt)
print('Final X speed: %.2f m/s' % velX)
print('Final X distance: %.2f m' % distX)
print('Average X speed: %.2f m/s' % avgVelX)

