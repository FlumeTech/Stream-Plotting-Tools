# Stream-Plotting-Tools
Helper tools for plotting raw data stream logs easily

# Dependencies
Stream-Plotting-Tools utilizes the matplotlib module for generating fancy labeled plots. We also utilize scipy for curvefitting. Below is a list of all modules utilized:
[pickle](https://docs.python.org/3/library/pickle.html#module-pickle)
[matplotlib](https://matplotlib.org/)
[numpy](https://numpy.org/)
[scipy](https://scipy.org/)

This program was developed and tested on Python 3.8.10, other versions of python3 are not guaranteed to work.

# Usage
Call the program from the command line:
```
$:~python3 ./streamPlotter.py
streamPlotter.py USAGE:
--type=<mag, atmo>
--file=<path to file>
--process=<humidity_testing - find the point in the splot where the temprature bottoms out and start the run from that point.>
--labels=<labels for various plots if you don't want the default label>
```

## Arguments
Types of streams accepted are mag (normal magnetometer data), and atmo (atmospheric sensor data).
Files are raw stream logs, which are expected to be in the format of Flume raw data stream logs from the [streaming server](https://admin.flume.us/streams/files/). You can include multiple stream logs by seperating them via comma in the command line.
Processes are only `humidity_testing` at this time, which is designed to truncate the atmospheric sensor logs at the lowest stable temperature.
Labels is a comma separated list of custom labels for each log associated.

# Example Usage and Output
```
python3 ./streamPlotter.py --type=atmo --file=/Path/To/Logs/H1\ Bakeoff\ to\ Env\ Plastic\ Coated\ with\ Humiseal\ \&\ Oring\ Epoxy.log,/Path/To/Logs/H1\ Bakeoff\ to\ Env\ Plastic\ Coated\ with\ Humiseal.log,/Path/To/Logs/H1\ Bakeoff\ to\ Env\ Wood\ Sandwich\ Clamp.log,/Path/To/Logs/H1\ Bakeoff\ to\ Env\ Wood\ Sandwich\ Clamp\ Viton.log,/Path/To/Logs/H1\ Bakeoff\ to\ Env\ Baseline.log --process=humidity_testing --labels=Humiseal_And_Epoxy,Humiseal,Clamped,Clamped_Viton,Baseline
processing humidity_testing
temperature range: 41.0 to 42.0
pressure range: 104.0 to 105.0
relative humidity range: 25.0 to 27.0
humidity rate range: -1.184085707593844e-06 to 4.838192477924328e-05
temperature range: 40.0 to 44.0
pressure range: 99.0 to 102.0
relative humidity range: 23.0 to 38.0
humidity rate range: 4.248366506038863e-05 to 0.00016571241061440464
temperature range: 41.0 to 43.0
pressure range: 100.0 to 101.0
relative humidity range: 13.0 to 22.0
humidity rate range: 8.435909806693444e-05 to 0.00011153012227794672
temperature range: 41.0 to 44.0
pressure range: 97.0 to 99.0
relative humidity range: 11.0 to 23.0
humidity rate range: 5.502753275646412e-05 to 7.202449335269759e-05
temperature range: 40.0 to 41.0
pressure range: 99.0 to 100.0
relative humidity range: 27.0 to 41.0
humidity rate range: 6.636478375586068e-05 to 0.0003054364734838229
```

![H1 Comparison Latest](https://user-images.githubusercontent.com/6101274/182236403-e1c0ff9e-d9eb-4cfd-a0c4-f51386d80930.png)
