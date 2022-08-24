
#!/usr/bin/python3
from pickle import FALSE, TRUE
import sys
import getopt
import matplotlib.pyplot as plt 
from statistics import mean
from tabulate import tabulate
# fit a straight line to the economic data
from numpy import arange
from scipy.optimize import curve_fit
import numpy as np

import streamData as sd
import humidityTesting as ht
import presenter as pr

class humCurveFitting:
    xLine = []
    yLine = []
    yPrime = []

    def __init__(self):
        self.xLine = []
        self.yLine = []
        self.yPrime = []

def printArgHelp():
    print("streamPlotter.py USAGE:")
    print("--type=<mag, atmo, rh_comp>")
    print("--file=<path to file>")
    print("--process=<humidity_testing - find the point in the splot where the temprature bottoms out and start the run from that point.>")
    print("--labels=<labels for various plots if you don't want the default label>")

def helper_func(ele):
        name, val = ele.split()
        return val

def main(argv):
    ## Check the args
    if len(argv) < 1:
        printArgHelp()
        sys.exit(2)

    try:
        opts, _ = getopt.getopt(argv, "-h",["type=","file=","process=", "labels="])
    except getopt.GetoptError:
        printArgHelp()
        sys.exit(2)

    # Parse the args
    type = "mag"
    process = "none"
    labels = []
    for opt, arg in opts:
        if opt == '-h':
            printArgHelp()
            sys.exit()
        elif opt == "--type":
            type = arg
        elif opt == "--file":
            # If we have multiple files, we need to compare them
            files = []
            f = arg.split(",")
            for i in f:
                files.append(i)
        elif opt == "--process":
            process = arg
        elif opt == "--labels":
            f = arg.split(",")
            for i in f:
                labels.append(i)

    # Screen the types
    if type != "mag" and type != "atmo" and type != "rh_comp":
        print("Invalid type: " + type)
        sys.exit(2)
    
    # Create a list of streamData objects
    data = []

    # Populate the list of streamData objects
    maxLines = 5000000
    try:
        k = 0
        for i in files:
            # Read the file into a buffer
            f = open(i, "r")
            buf = f.read()
            f.close()

            # Make a streamData object
            data.append(sd.streamData())

            # Split the buffer into lines
            j = 0
            for line in buf.split("\n"):
                j += 1
                if j > maxLines:
                    print("Warning: File " + i + " has more than " + str(maxLines) + " lines. Skipping the rest.")
                    break
                if j <= 4:
                    continue
                field = line.split(",")
                if len(field) < 4:
                    continue
                
                # Set the record
                data[k].setRecord(float(field[0]) / 1000.0, float(field[1]), float(field[2]), float(field[3]))
            
            k += 1
    except:
        print("Error reading file: " + i)
        sys.exit(2)

    # Process data if we are doing a certain type of processing
    if process == "humidity_testing":
        # Loop through the data, clip it, and fit it
        processedData = []
        fitData = []
        for i in data:
            # Clip and fit the data
            clip, hum = ht.fixedTempAndHumidityProcess(i)
            processedData.append(clip)
            fitData.append(hum)

        if type == "atmo":
            # Display the data and return
            pr.presentFixedTempAndHumData(processedData, fitData, labels)
        elif type == "rh_comp":
            # Display the data and return
            pr.presentRHComparison(processedData, fitData, labels)
    else:
        if type == "atmo":
            # Present the data
            pr.presentRawAtmoData(data, labels)
        elif type == "mag":
            # Present the data
            pr.presentRawMagData(data, labels)

if __name__ == "__main__":
    main(sys.argv[1:])