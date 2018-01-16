import csv
import math
import time

from collections import defaultdict

import os
#from os import path




#	# eventual cartesian to spherical conversion
#import numpy as np
#
#def appendSpherical_np(xyz):
#	ptsnew = np.hstack((xyz, np.zeros(xyz.shape)))
#	xy = xyz[:,0]**2 + xyz[:,1]**2
#	ptsnew[:,3] = np.sqrt(xy + xyz[:,2]**2)
#	ptsnew[:,4] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
#	#ptsnew[:,4] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
#	ptsnew[:,5] = np.arctan2(xyz[:,1], xyz[:,0])
#	return ptsnew
#


baseUnit = {
	"microMeter" : 10**(-6), 
	"milliMeter" : 10**(-5),
 	"centiMeter" : 10**(-4) 
 	}

baseUnitToUse = "microMeter"

# do not write header to CSV, (Rhino/GH doesnt like it)
writeOutCSVHeader = False 

# should the script generate reference positions for the points?
generateRefPositionFile = False 

dir = os.path.dirname(__file__)
timestr = time.strftime("%Y%m%d-%H%M%S")

log10FileName = 'output/positions-{}-log10.csv'.format(timestr)
linearFileName = 'output/positions-{}-linear.csv'.format(timestr)

try:	
	with open(os.path.join(dir, "..","..","datalogs","20180115-16h57m.CSV"), newline='') as in_csvfile, \
		 open(log10FileName, 'w') as log10_out_csvfile, \
		 open(linearFileName.format(timestr), 'w') as linear_out_csvfile:
		
		# columns for output CSV file
		fieldnames = ['posX', 'posY', 'posZ']
	
		# initialize writer
		log10_posData = csv.DictWriter(log10_out_csvfile, fieldnames=fieldnames)
		linear_posData = csv.DictWriter(linear_out_csvfile, fieldnames=fieldnames)
	
		# write column names to output CSV file
		if writeOutCSVHeader:
			log10_posData.writeheader()
			linear_posData.writeheader()

		# read rows into a dictionary format
		IMUData = csv.DictReader(in_csvfile) 
	
		# I/O fieldnames
		print("Input fieldnames are " + str(IMUData.fieldnames))
		print("Output fieldnames are " + str(log10_posData.fieldnames), end="")
		print(" and are ", end="")
		if writeOutCSVHeader == False:
			print("NOT ", end="")
		print("being written.")

		print("\n")
	
		#starting vars
		velX, velY, velZ = 0, 0, 0
		posX, posY, posZ = 0, 0, 0
		distX, distY, distZ = 0, 0, 0
		previousAccX, previousAccY, previousAccZ = 0, 0, 0
		logPosX, logPosY, logPosZ = 0, 0, 0
	
		previousTimestamp = 0
		dataPointCt = 0
	
		print("GO!\n\n")
	
		for row in IMUData:
	
			# deltaT = (current timestap - last timestamp)
			# divided by 1000 to convert from millis to seconds
			deltaT = float(row['timestamp'])/1000.0
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
			
			#print('posX: %.6f,\tposY: %.6f,\tposZ: %.6f,\tdT: %.4f' % (posX, posY, posZ, deltaT))
			print(".", end="")

			# create new vars to manipulate as logs
			logPosX = posX
			logPosY = posY
			logPosZ = posZ

			# if conversion to log would render a negative log, make this number = to log10(1).
			if (abs(logPosX)/baseUnit[baseUnitToUse]) < 1:
					if logPosX < 0:
						logPosX = -1*baseUnit[baseUnitToUse]
					else:
						logPosX = 1*baseUnit[baseUnitToUse]
			
			if (abs(logPosY)/baseUnit[baseUnitToUse]) < 1:
					if logPosY < 0:
						logPosY = -1*baseUnit[baseUnitToUse]
					else:
						logPosY = 1*baseUnit[baseUnitToUse]
			
			if (abs(logPosZ)/baseUnit[baseUnitToUse]) < 1:
					if logPosZ < 0:
						logPosZ = -1*baseUnit[baseUnitToUse]
					else:
						logPosZ = 1*baseUnit[baseUnitToUse]
			

			# now convert from linear to log
			# if the distance is negative, convert to positive,
			# do log conversion, and then make negative again
			if logPosX < 0:
				logPosX = math.log10(abs(logPosX/baseUnit[baseUnitToUse])) * (-1)
			else:
				logPosX = math.log10(abs(logPosX/baseUnit[baseUnitToUse]))
			
			if logPosY < 0:
				logPosY = math.log10(abs(logPosY/baseUnit[baseUnitToUse])) * (-1)
			else:
				logPosY = math.log10(abs(logPosY/baseUnit[baseUnitToUse]))
			
			if logPosZ < 0:
				logPosZ = math.log10(abs(logPosZ/baseUnit[baseUnitToUse])) * (-1)
			else:
				logPosZ = math.log10(abs(logPosZ/baseUnit[baseUnitToUse]))
	
	
	
			# write datapoints do file until u have 10k points, then break out of loop
			if dataPointCt < 10000:
				# output info to CSVs
				log10_posData.writerow({
					'posX': '%0.6f' % logPosX,
					'posY': '%0.6f' % logPosY,
					'posZ': '%0.6f' % logPosZ
					})
	
				linear_posData.writerow({
					'posX': '%0.6f' % posX,
					'posY': '%0.6f' % posY,
					'posZ': '%0.6f' % posZ
					})
	
			else:
				break #break out of loop


	# average speed calculation, assumes first timestamp = 0
	avgVelX = posX/100#(previousTimestamp/1000)
	avgVelY = posY/100#(previousTimestamp/1000)
	avgVelZ = posZ/100#(previousTimestamp/1000)
	
	
	print('\nIntegrated %i data points.\n' % dataPointCt)
	
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
	
except:
	print("Some error occurred...")
	# deletes empty files if any where created
	if os.stat(log10FileName).st_size == 0:
		os.remove(log10FileName)
	if os.stat(linearFileName).st_size == 0:
		os.remove(linearFileName)




if generateRefPositionFile:
	# will be viewed linearly in ""log space""
	with open('output/refPos-{}-log10.csv'.format(timestr), 'w') as out_csvreffile:
	
		# columns for output CSV file
		fieldnames = ['refPosX', 'refPosY', 'refPosZ']
	
		# initialize writer
		refPosData = csv.DictWriter(out_csvreffile, fieldnames=fieldnames)
	
		for x in range(-2,2):
			for y in range(-2,2):
				for z in range(-2,2):

					logRefPosX = 10**(x*3)
					logRefPosY = 10**(y*3)
					logRefPosZ = 10**(z*3)
			
					#print('posX: \t%.6f,\tposY: \t%.6f,\tposZ: \t%.6f,' % (refPosX, refPosY, refPosZ))
			
					logRefPosX = math.log10(abs(logRefPosX/baseUnit[baseUnitToUse]))
					logRefPosY = math.log10(abs(logRefPosY/baseUnit[baseUnitToUse]))
					logRefPosZ = math.log10(abs(logRefPosZ/baseUnit[baseUnitToUse]))
			
					print('Log - posX: %.1f,\tposY: %.1f,\tposZ: %.1f,' % (logRefPosX, logRefPosY, logRefPosZ))
			
					# output info to CSV
					refPosData.writerow({
						'refPosX': '%0.6f' % logRefPosX,
						'refPosY': '%0.6f' % logRefPosY,
						'refPosZ': '%0.6f' % logRefPosZ
						})

	# will be viewed logarythmicaly in ""log space""
	with open('output/refPos-{}-linear.csv'.format(timestr), 'w') as out_csvreffile:
	
		# columns for output CSV file
		fieldnames = ['refPosX', 'refPosY', 'refPosZ']
	
		# initialize writer
		refPosData = csv.DictWriter(out_csvreffile, fieldnames=fieldnames)
		for p in range(0, 1):
			for x in range(1,1000):
				for y in range(1,2):
					for z in range(1,2):
	
						refPosX = x*0.000001*(10**(p*3))
						refPosY = y*0.000001*(10**(p*3))
						refPosZ = z*0.000001*(10**(p*3))
				
						#print('posX: \t%.6f,\tposY: \t%.6f,\tposZ: \t%.6f,' % (refPosX, refPosY, refPosZ))
						logRefPosX = math.log10(abs(refPosX/baseUnit[baseUnitToUse]))
						logRefPosY = math.log10(abs(refPosY/baseUnit[baseUnitToUse]))
						logRefPosZ = math.log10(abs(refPosZ/baseUnit[baseUnitToUse]))
				
						print('Linear - posX: %.4f,\tposY: %.4f,\tposZ: %.4f,' % (logRefPosX, logRefPosY, logRefPosZ))
				
						# output info to CSV
						refPosData.writerow({
							'refPosX': '%0.6f' % logRefPosX,
							'refPosY': '%0.6f' % logRefPosY,
							'refPosZ': '%0.6f' % logRefPosZ
							})

	print("ref positions file generated")


