
# Drift a part




#Python:

	Validation:
	(as in, can random acceleration data generate interesting shapes? If yes, continue)
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
		 	(use previous mockData to test script, should generate hand calculated data for multiple data points)
		 - Script to generate random mock data
		 - Generate positions and view on 3D Space from of CSV (Rhino and Web)

		 - Next issue: 
		 	Would it continue to be interesting with real data?



	Validation:
	(can real noise from acceleration data generate interesting shapes? If yes, continue)
		 - Hardware/Firmware/Mechanical development
		 - Import real data
		 - Export positions into 3D Space from CSV (Rhino)
		 - Heavy skew into Vertical Axis
		 	(I speculate that it is because its the axis that is suffering constant 1g force and therefore drifting much more)
		 - Implementation of "High Pass" filter 
		 	(subtracting rolling average of current reading,
		 	previous implementation was just calculating local G from n readings during boot)

		 - Next issue: 
		 	It generates interesting shapes but unrecognizable in a linear scale.
		 	The overal shape is almost a straight line, and there are interesting movements zooming in 1000 times, 1000000 times.
		 	All cannot be seen at the same time.
			Is it possible to conciliate these different scales?

	
	Validation:
	


#Firmware:

	 - Testing IMU via Interrupt driven SPI to Serial Port
	 - Testing IMU via Interrupt driven SPI to Serial Port and SD Card
	 - Testing dataset
	 - Implementing gravity "High Pass" filter
	
	Minor corrections such as data format, header, sample intervals, etc not included.