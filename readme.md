
# Drift a part


## Steps

### Python:

Validation:
Can __random acceleration__ data generate interesting shapes?

	 - Script to generate mock data with predictable/calculatable results 
	 	(i.e.: 
	 		AccelX: 10m/sˆ2
	 		deltaTime = 1 second
	 		=> 
	 			deltaSpeedX of 10m/s (from AccelX * deltaTime)
	 			=>
	 				initSpeedX = 0 m/s
					finalSpeedX = initSpeedX + deltaSpeedX = 10m/s
					averageSpeedX = deltaSpeedX/2
					deltaDistanceX = deltaSpeedX * deltaTime = 5m)
	 - Script to integrate acceleration data into Speed and Speed into positions
	 	use previous mockData to test script, 
	 	should generate hand calculated data for multiple data points)
	 - Script to generate random mock data
	 - Generate positions and view on 3D Space from of CSV (Rhino and Web)

	 - Next issue: 
	 	Would it continue to be interesting with real data?



Validation:
Can **real noise from acceleration data** generate interesting shapes?

	 - Hardware/Firmware/Mechanical development
	 - Import real data
	 - Export positions into 3D Space from CSV (Rhino)
	 - Heavy skew into Vertical Axis
	 	(I speculate that it is because its the axis that is suffering constant 1g
	 	and therefore drifting much more)
	 - Implementation of "High Pass" filter 
	 	(subtracting rolling average of current reading,
	 	previous implementation was just calculating local G from n readings during boot)

	 - Next issue: 
	 	It generates interesting shapes but unrecognizable in a linear scale.
	 	The overal shape is almost a straight line, and there are interesting
	 	movements zooming in 1000 times, 1000000 times.
	 	All cannot be seen at the same time.
		Is it possible to conciliate these different scales?


Validation:
Can **log-log graphs**, make the interesting shapes in different scales all visible at the same time in 3D space?

	 - Implementation of log() conversion in Cartesian (XYZ) space.
	 	(log operation is done on each axis individually,
	 	this results in a heavy distortion of the shape, 
	 	it always crosses the quadrant planes perpendicularlly)
	 - Correction of log() implementation, now using Spherical (Radius, elevation, Azimuth) space.
	 	(log operation is done only on radius)
	


### Firmware:

	 - Testing IMU via Interrupt driven SPI to Serial Port
	 - Testing IMU via Interrupt driven SPI to Serial Port and SD Card
	 - Testing dataset
	 - Implementing gravity "High Pass" filter
	
	Minor corrections such as data format, header, sample intervals, etc not included.