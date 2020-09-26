import os
import shutil

'''
Maggie Xu, Vaanyi Igiri, Aleksandar Vranjes
CMPT 353 Project using OSM data

A simple program to clean the exported files after an execution of the program. (Optional)
'''

# Remove files in home directory
if os.path.exists("filtered_amenities.csv"):
	os.remove("filtered_amenities.csv")
else:
	print("---The file 'filtered_amenities.csv' does not exist.") 

if os.path.exists("close_amenities.csv"):
	os.remove("close_amenities.csv")
else:
	print("---The file 'close_amenities.csv' does not exist.")

if os.path.exists("path_travelled.csv"):
	os.remove("path_travelled.csv")
else:
	print("---The file 'path_travelled.csv' does not exist.")

if os.path.exists("planned_route.html"):
	os.remove("planned_route.html")
else:
	print("---The file 'planned_route.html' does not exist.")

if os.path.exists("van_heatmap.html"):
	os.remove("van_heatmap.html")
else:
	print("---The file 'van_heatmap.html' does not exist.")

if os.path.exists("your_route.html"):
	os.remove("your_route.html")
else:
	print("---The file 'your_route' does not exist.")

if os.path.exists("smoothed.gpx"):
	os.remove("smoothed.gpx")
else:
	print("---The file 'smoothed.gpx' does not exist.")

if os.path.exists("unsmoothed.gpx"):
	os.remove("unsmoothed.gpx")
else:
	print("---The file 'unsmoothed.gpx' does not exist.")

# Remove folders cache and pycache
try:
    shutil.rmtree("cache")
except OSError as e:
    print ("---Error: %s - %s." % (e.filename, e.strerror))

try:
    shutil.rmtree("__pycache__")
except OSError as e:
    print ("---Error: %s - %s." % (e.filename, e.strerror))

print("\n---All other files/folders have successfully been removed.")
    

