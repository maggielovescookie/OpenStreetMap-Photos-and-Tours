import numpy as np
import pandas as pd
import sys
import time

'''
Maggie Xu, Vaanyi Igiri, Aleksandar Vranjes
CMPT 353 Project using OSM data

This program gives the user a choice of what kind of amenities they want to see on their tour.
'''

def main(input_csv):
	'''
	Present to the user what kind of amenities they could see.
	'''
	print('\n')
	# Read input csv file into Pandas DataFrame
	a = pd.read_csv(input_csv)

	# List of options for easy printing later
	options = ["1. Food and Drink", \
			   "2. Academic", \
		       "3. Religious", \
			   "4. Healthcare/Childcare/Petcare", \
			   "5. Entertainment", 
			   "6. Community", \
			   "7. Postal Services", \
		       "8. Car Utility", \
		       "9. Bike/Motorcycle Utility", \
		       "10. Transportation", \
			   "11. Bars/Pubs/Clubs", \
			   "12. Leisure", \
			   "13. Finance", \
			   "14. Park/Recreation", \
			   "15. Waste Disposal/Washrooms", \
			   "16. Miscellaneous",\
			   "17. All"]

	print("Amenities up to a distance of 100 metres to all photos have been filtered.")

	invalid_option = True

	# User input processing: Filter the DataFrame based on the amenities we're looking for
	while(invalid_option):
		try:
			print("What kind of amenities would you like to see on your tour?\n")
			print(options[0] + "\n" + \
		  		  options[1] + "\n" + \
		  		  options[2] + "\n" + \
		  		  options[3] + "\n" + \
		 		  options[4] + "\n" + \
		  		  options[5] + "\n" + \
		  		  options[6] + "\n" + \
		  		  options[7] + "\n" + \
		  		  options[8] + "\n" + \
		  		  options[9] + "\n" + \
		  		  options[10] + "\n" + \
				  options[11] + "\n" + \
				  options[12] + "\n" + \
				  options[13] + "\n" + \
				  options[14] + "\n" + \
				  options[15] + "\n" + \
			      options[16])

			number = input("Please enter an option number:\n")

			number = int(number) # Convert to int

			if number == 1:
				invalid_option = False
				new_a = a[(a['amenity'] == 'restaurant') | (a['amenity'] == 'cafe') | (a['amenity'] == 'fast_food') | (a['amenity'] == 'ice_cream') | (a['amenity'] == 'bistro') | (a['amenity'] == 'food_court') | (a['amenity'] == 'marketplace') | (a['amenity'] == 'juice_bar')]
			elif number == 2:
				invalid_option = False
				new_a = a[(a['amenity'] == 'school') | (a['amenity'] == 'college') | (a['amenity'] == 'university') | (a['amenity'] == 'cram_school') | (a['amenity'] == 'kindergarten') | (a['amenity'] == 'driving_school') | (a['amenity'] == 'language_school') | (a['amenity'] == 'music_school') | (a['amenity'] == 'prep_school') | (a['amenity'] == 'research_institute') | (a['amenity'] == 'school') | (a['amenity'] == 'workshop')]
			elif number == 3:
				invalid_option = False
				new_a = a[(a['amenity'] == 'place_of_worship') | (a['amenity'] == 'monastery')]
			elif number == 4:
				invalid_option = False
				new_a = a[(a['amenity'] == 'dentist') | (a['amenity'] == 'doctors') | (a['amenity'] == 'childcare') | (a['amenity'] == 'clinic') | (a['amenity'] == 'nursery') | (a['amenity'] == 'chiropractor') | (a['amenity'] == 'first_aid') | (a['amenity'] == 'healthcare') | (a['amenity'] == 'hospital') | (a['amenity'] == 'pharmacy') | (a['amenity'] == 'safety') | (a['amenity'] == 'veterinary') | (a['amenity'] == 'animal_shelter')]
			elif number == 5:
				invalid_option = False
				new_a = a[(a['amenity'] == 'cinema') | (a['amenity'] == 'theatre') | (a['amenity'] == 'casino') | (a['amenity'] == 'events_venue') | (a['amenity'] == 'gambling') | (a['amenity'] == 'photo_booth') | (a['amenity'] == 'social_centre') | (a['amenity'] == 'internet_cafe')]
			elif number == 6:
				invalid_option = False
				new_a = a[(a['amenity'] == 'community_centre') | (a['amenity'] == 'library') | (a['amenity'] == 'arts_centre') | (a['amenity'] == 'police') | (a['amenity'] == 'public_bookcase') | (a['amenity'] == 'public_building') | (a['amenity'] == 'ranger_station') | (a['amenity'] == 'townhall') | (a['amenity'] == 'arts_centre') | (a['amenity'] == 'courthouse') | (a['amenity'] == 'family_centre') | (a['amenity'] == 'fire_station')]
			elif number == 7:
				invalid_option = False
				new_a = a[(a['amenity'] == 'post_box') | (a['amenity'] == 'post_office') | (a['amenity'] == 'letter_box') | (a['amenity'] == 'post_depot')]
			elif number == 8:
				invalid_option = False
				new_a = a[(a['amenity'] == 'car_rental') | (a['amenity'] == 'car_sharing') | (a['amenity'] == 'car_rep') | (a['amenity'] == 'car_wash') | (a['amenity'] == 'charging_station') | (a['amenity'] == 'driving_school') | (a['amenity'] == 'fuel') | (a['amenity'] == 'parking') | (a['amenity'] == 'parking_entrance') | (a['amenity'] == 'parking_space')]
			elif number == 9:
				invalid_option = False
				new_a = a[(a['amenity'] == 'bicycle_rental') | (a['amenity'] == 'bicycle_parking') | (a['amenity'] == 'motorcycle_parking') | (a['amenity'] == 'bicycle_repair_station') | (a['amenity'] == 'Motorcycle_rental')]
			elif number == 10:
				invalid_option = False
				new_a = a[(a['amenity'] == 'bus_station') | (a['amenity'] == 'ferry_terminal') | (a['amenity'] == 'seaplane_terminal') | (a['amenity'] == 'taxi') | (a['amenity'] == 'trolley_bay') | (a['amenity'] == 'loading_dock') | (a['amenity'] == 'boat_rental')]
			elif number == 11:
				invalid_option = False
				new_a = a[(a['amenity'] == 'bar') | (a['amenity'] == 'biergarten') | (a['amenity'] == 'pub') | (a['amenity'] == 'nightclub') | (a['amenity'] == 'lounge') | (a['amenity'] == 'stripclub')]
			elif number == 12:
				invalid_option = False
				new_a = a[(a['amenity'] == 'leisure') | (a['amenity'] == 'lounge') | (a['amenity'] == 'social_centre') | (a['amenity'] == 'spa') | (a['amenity'] == 'meditation_centre')]
			elif number == 13:
				invalid_option = False
				new_a = a[(a['amenity'] == 'atm') | (a['amenity'] == 'bank') | (a['amenity'] == 'bureau_de_change') | (a['amenity'] == 'money_transfer') | (a['amenity'] == 'payment_terminal')]
			elif number == 14:
				invalid_option = False
				new_a = a[(a['amenity'] == 'bbq') | (a['amenity'] == 'bench') | (a['amenity'] == 'drinking_water') | (a['amenity'] == 'fountain') | (a['amenity'] == 'community_centre') | (a['amenity'] == 'gym') | (a['amenity'] == 'playground') | (a['amenity'] == 'shelter') | (a['amenity'] == 'watering_place') | (a['amenity'] == 'water_point') | (a['amenity'] == 'park')]
			elif number == 15:
				invalid_option = False
				new_a = a[(a['amenity'] == 'recycling') | (a['amenity'] == 'sanitary_dump_station') | (a['amenity'] == 'toilets') | (a['amenity'] == 'trash') | (a['amenity'] == 'vacuum_cleaner') | (a['amenity'] == 'scrapyard') | (a['amenity'] == 'waste_basket') | (a['amenity'] == 'waste_disposal') | (a['amenity'] == 'waste_transfer_station')]
			elif number == 16:
				invalid_option = False
				new_a = a[(a['amenity'] == 'compressed_air') | (a['amenity'] == 'bench') | (a['amenity'] == 'conference_centre') | (a['amenity'] == 'construction') | (a['amenity'] == 'smoking_area') | (a['amenity'] == 'telephone') | (a['amenity'] == 'vending_machine') | (a['amenity'] == 'dojo')]
			elif number == 17:
				invalid_option = False
				new_a = a
			else:
				print("\n---Invalid input. Please input a number from 1 to 16.\n")
				time.sleep(1)

		# Value error exception catching
		except ValueError:
			print("\n---Invalid input. Please input a number from 1 to 16.\n")
			time.sleep(1)

	# If the DataFrame is empty, there are none of the chosen amenities nearby
	if new_a.empty:
		print("\n---There are none of the chosen amenities nearby your path.")
	else:
		print("\n---Printed to filtered_amenities.csv.")

		# Sort the DataFrame by amenity name and output to csv
		new_a = new_a[new_a['name'].notna()]
		new_a_grouped = new_a.sort_values(by=['amenity'])
		new_a_grouped = new_a_grouped.rename(columns={'am_lat': 'lat', 'am_lon': 'lon'})

		new_a_grouped.to_csv('filtered_amenities.csv')


if __name__ == '__main__':
    input_csv = sys.argv[1]
    main(input_csv)