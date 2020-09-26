import findspark
findspark.init()
findspark.find()
import pyspark
findspark.find()

import numpy as np
import pandas as pd
import sys
import warnings

from getRoute import deg2rad
from pyspark.sql import SparkSession, functions, types, Row
from pyspark import SparkContext, SparkConf

'''
Maggie Xu, Vaanyi Igiri, Aleksandar Vranjes
CMPT 353 Project using OSM data

This program takes the output csv from getRoute.py (path_travelled.csv) and loads it in a Pandas DataFrame. It then loads the 
OSM data from amenities-vancouver.json.gz into a Pyspark DataFrame and converts to Pandas. Finally, it calculates the distance
from all coordinates in the amenities DataFrame to that of the path_travelled DataFrame to see what amenities are within 100m
of the path points given.
'''

conf = pyspark.SparkConf().setAppName('close amenities').setMaster('local')
sc = pyspark.SparkContext(conf=conf)
spark = SparkSession(sc)

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

warnings.simplefilter(action='ignore')

################ JSON file schema #####################
schema = types.StructType([
    types.StructField('lat', types.FloatType()),
    types.StructField('lon', types.FloatType()),
    types.StructField('timestamp', types.StringType()),
    types.StructField('amenity', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('tags', types.StringType()),
])

def main(dataset, path_dataset, out_directory):
	'''
	Find all amenities within 100m of the given set of photo coordinates.
	'''
	av = spark.read.json(dataset, schema=schema)
	av.cache()

	amenity_df = av.select("*").toPandas() # Convert to Pandas df
	pt = pd.read_csv(path_dataset)#, sep='delimiter') # Dataframe exported from getRoute

	# Calculate the distance between points in path_travelled.csv and points in amenity_df.
	combined_df = amenity_df.assign(key=1).merge(pt.assign(key=1), how='outer', on='key')

	R = 6371

	dLat = deg2rad(combined_df['lat_y']-combined_df['lat_x'])
	dLon = deg2rad(combined_df['lon_y']-combined_df['lon_x'])

	a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(deg2rad(combined_df['lat_x'])) * np.cos(deg2rad(combined_df['lat_y'])) * np.sin(dLon/2) * np.sin(dLon/2)
    
	c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
	d = R * c * 1000 # Distance in m

	combined_df['distance(m)'] = d
	combined_df=combined_df.sort_values(['distance(m)']) # Lat/lon_y are the coordinates from pt

	tmp = combined_df.loc[(combined_df['distance(m)'] <= 100)] # Includes only amenities within 100m
	tmp.rename(columns={'lat_x': 'am_lat', 'lon_x': 'am_lon', 'lat_y': 'photo_lat', 'lon_y': 'photo_lon'}, inplace=True)

	tmp.to_csv(out_directory)  # Amenities within 100m of 1 or more coordinates given by the photos

	sc.stop()


if __name__ == '__main__':
    dataset = sys.argv[1]
    path_dataset = sys.argv[2]
    out_directory = sys.argv[3]
    main(dataset, path_dataset, out_directory)

