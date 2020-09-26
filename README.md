# CMPT 353 Project
## OpenStreetMap, Photos, and Tours
### Maggie Xu, Vaanyi Igiri, Aleksandar Vranjes

For a list of all modules/packages needed to run the code, see **requirements.txt**.
All data used for the Airbnb processing is in the data folder; the OSM json file is in the osm folder.

To run the system, use **main.py** with the following arguments:

	$ python3 main.py 'large_dataset_folder' '/path/to/photos/folder/'

Example:

	$ python3 main.py osm /home/aleks/Documents/cmpt-353/cmpt-353-project/van-tour-photos

When running option 1, the final csv file containing the chosen amenities is **filtered_amenities.csv**. The html file showing your tour path and the location of the amenities you have chosen will be **your_route.html**.

When running option 2, the gpx files exported will be **unsmoothed.gpx** and **smoothed.gpx**.

When running option 3, the final html map showing your planned route is **planned_route.html**.

The names of all output files can be seen in the delete.py file. There are csv files, gpx files, and html files exported depending on what option you decide to execute in main.py.

To clean up all files/folders exported after execution of the program, simply run **delete.py**:

	$ python3 delete.py
