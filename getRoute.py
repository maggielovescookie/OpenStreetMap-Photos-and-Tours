import exifread
import glob
import numpy as np
import pandas as pd
import sys
from datetime import datetime
from pykalman import KalmanFilter
import osmnx as ox
import networkx as nx
import folium

'''
Maggie Xu, Vaanyi Igiri, Aleksandar Vranjes
CMPT 353 Project using OSM data

This program creates a Pandas DataFrame with the time, latitude, and longitude EXIF info from the metadata
of a collection of photos in a folder. It then exports this DataFrame as a csv (path_travelled.csv) to be
used in other programs.

Optionally, it can calculate the distance between all photos, smooth the distance using a Kalman filter, and 
even export gpx files of both the smoothed and unsmoothed points to visualize the user's tour io a GPS map.

The 'deg2rad' function is referenced in closeAmenities.py and tourPlanning.py.
'''

def get_exif(photo):
    '''
    Retrieve exifinfo from a set of photos in the given path.
    '''
    with open(photo, 'rb') as f:
        tags = exifread.process_file(f)
    try:
        Time = tags['EXIF DateTimeOriginal'].printable
        # latitude
        lat_ref = tags["GPS GPSLatitudeRef"].printable
        lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
        if lat_ref != "N":
            lat = lat * (-1)
        # longtitude
        lon_ref = tags["GPS GPSLongitudeRef"].printable
        lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        lon = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600
        if lon_ref != "E":
            lon = lon * (-1)
    except KeyError:
        return "ERROR:The image do not include EXIF info."
    else:
        #print("Time: ", Time, "\n", "latitude: ", lat, "longtitude: ", lon)
        return {"time": Time, "lat": lat, "lon": lon}


def deg2rad(deg) :
    '''
    Change degree value to radians. (Based on Exercise 3)
    '''
    return deg * (np.pi/180)


def distance(points):
    '''
    Find the distance between two given points of longitude and latitude. (Based on Exercise 3)
    References: https://stackoverflow.com/questions/20095673/shift-column-in-pandas-dataframe-up-by-one
                https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
    '''
    points['lat2'] = points['lat'].shift(-1)
    points['lon2'] = points['lon'].shift(-1)
    points = points[:-1]

    R = 6371 # Radius of the earth in km

    dLat = deg2rad(points['lat2']-points['lat'])
    dLon = deg2rad(points['lon2']-points['lon'])

    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(deg2rad(points['lat'])) * np.cos(deg2rad(points['lat2'])) * np.sin(dLon/2) * np.sin(dLon/2)
    
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R * c * 1000 # Distance in m
    sum_d = sum(d)

    return sum_d


def smooth(points):
    '''
    Find the Kalman smoothed distance using the same points. (Based on Exercise 3)
    '''
    kalman_data = points[['lat', 'lon']]
    initial_state = kalman_data.iloc[0]

    # GPS can be accurate to about 5 metres but the reality seems to be several times that: maybe 15 or 20 metres with my phone.
    observation_covariance = np.diag([.0175, .0175]) ** 2 

    # Without any knowledge of what direction I was walking, we assume that my current position is the same as my previous position.
    transition_matrices = [[1, 0], [0, 1]] 

    # I usually walk something like 1 m/s and the data contains an observation about every 10 s. 
    transition_covariance = np.diag([0.01, 0.01]) ** 2 

    # Kalman Filter parameters
    kf = KalmanFilter(
        initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition_matrices
    )
    
    kalman_smoothed, _ = kf.smooth(kalman_data)

    # Create the kalman dataframe
    kalman_df = pd.DataFrame(data = kalman_smoothed[:], columns=['lat', 'lon'])

    return kalman_df


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame. (Based on Exercise 3)
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def mapRoute(points):
    
    #Reference: https://stackoverflow.com/questions/60578408/is-it-possible-to-draw-paths-in-folium
     
    ox.config(log_console=True, use_cache=True)
    
    G_walk = ox.graph_from_place('Vancouver, British Columbia, Canada', network_type='walk')   

    nodes = []
    routes = []

    for index, row in points.iterrows():
        nodes.append(ox.get_nearest_node(G_walk, (row['lat'], row['lon'])))
        if index > 0:
            routes.append(nx.shortest_path(G_walk, nodes[index-1], nodes[index],  weight='length'))
           
    for route in routes:
        route_map = ox.plot_route_folium(G_walk, route)
    
    return route_map
        

def main(path):
    '''
    Format dataframe using exifinfo from given photos, calculate distances, and output gpx/csv file(s).
    '''
    df = pd.DataFrame(columns=["time", "lat", "lon"])
    for image in glob.glob(path + '*.jpg'):
        df = df.append(get_exif(image), ignore_index=True)

    df = df.sort_values('time')

    # Raw distances between photos, output gpx
    points = df.drop(columns=['time']).reset_index() 
    
    # Output points DataFrame for usage in other programs: closeAmenities, etc
    points.to_csv('path_travelled.csv')


def main_gpx(path):
    '''
    Main clone, output gpx files and distance, no csv
    '''
    df = pd.DataFrame(columns=["time", "lat", "lon"])
    for image in glob.glob(path + '*.jpg'):
        df = df.append(get_exif(image), ignore_index=True)
    df = df.sort_values('time')

    points = df.drop(columns=['time']) 
    print('---Unfiltered distance between all photos: %0.2f' % (distance(points),))
    output_gpx(points, 'unsmoothed.gpx')
    smoothed_points = smooth(points)
    print('---Filtered distance between all photos: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'smoothed.gpx')

    print("---Unfiltered coordinates have been printed to: unsmoothed.gpx\n---Filtered coordinate have been printed to: smoothed.gpx")


if __name__ == '__main__':
    path = sys.argv[1]
    main(path)
