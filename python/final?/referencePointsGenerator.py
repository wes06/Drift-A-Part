import csv
import math

with open('output/refPos.csv', 'w') as out_csvreffile:
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