from weather_station import *
# DO NOT CHANGE ANY CODE ABOVE THIS LINE


# YOU MAY CHOOSE TO WRITE CODE HERE	

while NEW_DATA_AVAILABLE: # This is used to go to the next data reading
	site_label, temperature_reading = get_site_and_temperature_data()

	# YOUR CODE GOES HERE



	# YOU MAY USE THE BELOW FUNCTION TO CHECK YOUR SOLUTION
	show_grouped_site_and_temperature_data()
	