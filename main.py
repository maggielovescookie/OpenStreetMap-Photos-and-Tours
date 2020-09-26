import numpy as np
import pandas as pd
import sys
import time

import getRoute
import closeAmenities
import chooseAmenities
import tourPlanning
from getRoute import mapRoute
from tourPlanning import folium_markers

'''
Maggie Xu, Vaanyi Igiri, Aleksandar Vranjes
CMPT 353 Project using OSM data

This program runs the entire system.
Command line execution:
	$ python3 main.py 'large_dataset_folder' '/path/to/photos/folder/'

Example:
	$ python3 main.py osm /home/aleks/Documents/cmpt-353/cmpt-353-project/van-tour-photos
'''

def main(dataset, path_to_photos):
	'''
	Main menu processing
	'''
	print("\nWelcome to our OSM Project! What would you like to do:")

	invalid_option = True

	while(invalid_option):
		try:

			print("1. Find amenities within 100m of a given set of photos\n2. Create a smoothed tour given a set of photos\n3. Vancouver Airbnb tour")
			option = input("Please enter an option number:\n")
			option = int(option)

			if option == 1:
				# Calculate the route from a folder of photos and output a csv of the coordinates: path_travelled.csv
				# First system argument: the physical path from the /home/ directory to your folder of photos
				getRoute.main(path_to_photos)

    			# Find amenities within 100m of the given coordinates
    			# First system argument: the larger dataset of all amenities
    			# Second system argument: the name of the csv file to use from getRoute
    			# Third system argument: the name of the csv file output
				closeAmenities.main(dataset, "path_travelled.csv", "close_amenities.csv")

    			# Choose amenities; user input processing
    			# First system argument: the name of the csv file to use for choosing amenities, from closeAmenities
				chooseAmenities.main("close_amenities.csv")

				# Print the planned route and the nearby amenities to the photos onto an htmp map file
    			# (This functionality is not complete; it only maps the parts of your route that are in the city of Vancouver)
				m = mapRoute(pd.read_csv("path_travelled.csv"))
				m.add_child(folium_markers(pd.read_csv("filtered_amenities.csv")))
				m.save('your_route.html')

				print("\n---Amenities of the chosen kind have been printed to your_route.html.")

				invalid_option = False

			elif option == 2:
				# Calculate the route from a folder of photos and output the unfiltered vs filtered distance: smoothed and unsmoothed.gpx
				# First system argument: the physical path from the /home/ directory to your folder of photos
				getRoute.main_gpx(path_to_photos)

				invalid_option = False
				
			elif option == 3:

				# Start tour planning processing
				tourPlanning.main_menu()

				invalid_option = False

		# Value error exception catching
		except ValueError:
			print("\n---Invalid input. Please input 1, 2 or 3.\n")
			time.sleep(1)


if __name__ == '__main__':
	dataset = sys.argv[1]
	path_to_photos = sys.argv[2]
	main(dataset, path_to_photos)
