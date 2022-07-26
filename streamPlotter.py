
#!/usr/bin/python3
from pickle import FALSE, TRUE
import sys
import getopt
import matplotlib.pyplot as plt 
# fit a straight line to the economic data
from numpy import arange
from scipy.optimize import curve_fit

class streamData:
    time = []
    x = []
    y = []
    z = []

    def __init__(self):
        self.time = []
        self.x = []
        self.y = []
        self.z = []

    def setRecord(self, time, x, y, z):
        self.time.append(time)
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)

    def printRawData(self):
        for i in range(len(self.time)):
            print(self.time[i], self.x[i], self.y[i], self.z[i])

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
    print("--type=<mag, atmo>")
    print("--file=<path to file>")
    print("--process=<humidity_testing - find the point in the splot where the temprature bottoms out and start the run from that point.>")
    print("--labels=<labels for various plots if you don't want the default label>")

def linear(x, a, b):
    return a * x + b

def secondOrderPolynomial(x, a, b, c):
	return a * x + b * x**2 + c

def secondOrderPolynomialPrime(x, a, b):
    return a + 2 * b * x

def curveFitData(x, y):
    # Curve fit to the polynomial x^2, get the coefficients
    popt, _ = curve_fit(secondOrderPolynomial, x, y)
    a, b, c = popt

    # define a sequence of inputs between the smallest and largest known inputs
    dx = x[1] - x[0]
    x_line = arange(min(x), max(x), dx)

    # calculate the output for the range
    y_line = secondOrderPolynomial(x_line, a, b, c)

    # calculate the derivative of the output for the range
    y_prime = secondOrderPolynomialPrime(x_line, a, b)
    
    return x_line, y_line, y_prime

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
    if type != "mag" and type != "atmo":
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
            data.append(streamData())

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
    humidityRate = []
    if process == "humidity_testing":
        # For humidity testing, we need to find when the temperature stabilizes
        # in the humidity chamber, this is relatively easy to find because the temperature
        # bottoms out when it stabilizes.

        print("processing humidity_testing")

        processedData = []
        k = 0
        for i in data:
            processedData.append(streamData())

            # Find the temperature bottoms out
            temp = i.x[0]
            time = i.time[0]
            low = temp
            lowIndex = 0
            startTime = time
            for j in range(len(i.x)):
                if i.x[j] == low:
                    delta = i.time[j] - startTime
                    if delta > 3000:
                        lowIndex = j
                        break
                elif i.x[j] < low:
                    startTime = i.time[j]
                    low = i.x[j]
            # Cut the data from where the temperature bottoms out
            time = i.time[lowIndex:]
            x = i.x[lowIndex:]
            y = i.y[lowIndex:]
            z = i.z[lowIndex:]
            processedData[k].time = time
            processedData[k].x = x
            processedData[k].y = y
            processedData[k].z = z

            # Update the data field
            data[k] = processedData[k]

            # Grab the rates now
            humidityRate.append(humCurveFitting())
            xfit, yfit, yprimefit = curveFitData(time, z)
            humidityRate[k].xLine = xfit
            humidityRate[k].yLine = yfit
            humidityRate[k].yPrime = yprimefit
            k += 1

    # Make some plots
    if type == "atmo":
        timeList = []
        tempList = []
        pressList = []
        humList = []
        pnames = []
        colors = ["b","g","r","c","m","y","k"]
        otherColors = ["r","y","b","g","c","m"]
        j = 0
        for i in data:
            timeList.append(i.time)
            tempList.append(i.x)
            pressList.append(i.y)
            humList.append(i.z)
            if len(labels) > 0:
                pnames.append(labels[j])
            else:
                pnames.append("Atmo " + str(j))

            print("temperature range: " + str(min(tempList[j])) + " to " + str(max(tempList[j])))
            print("pressure range: " + str(min(pressList[j])) + " to " + str(max(pressList[j])))
            print("relative humidity range: " + str(min(humList[j])) + " to " + str(max(humList[j])))
            if process == "humidity_testing":
                print("humidity rate range: " + str(min(humidityRate[j].yPrime)) + " to " + str(max(humidityRate[j].yPrime)))

            j += 1
        # Create a subplot for each sensor
        try:
            # Create a figure with three subplots
            numSubPlots = 3
            if process == "humidity_testing":
                numSubPlots = 4

            fig, axs = plt.subplots(numSubPlots, 1)
            # Name the figure
            fig.suptitle("Atmospheric Data")
            # Plot temperature in subplot 0
            for i in range(len(tempList)):
                axs[0].scatter(timeList[i], tempList[i], label=pnames[i], color=colors[i])
            axs[0].set_title("Temperature (C)")
            axs[0].set_xlabel("Time (s)")
            axs[0].set_ylabel("°C")
            axs[0].legend()
            # Plot pressure in subplot 1
            for i in range(len(pressList)):
                axs[1].scatter(timeList[i], pressList[i], label=pnames[i], color=colors[i])
            axs[1].set_title("Pressure (KPa)")
            axs[1].set_xlabel("Time (s)")
            axs[1].set_ylabel("KPa")
            axs[1].legend()
            # Plot relative humidity in subplot 2
            for i in range(len(humList)):
                axs[2].scatter(timeList[i], humList[i], label=pnames[i], color=colors[i])
                if process == "humidity_testing":
                    axs[2].plot(humidityRate[i].xLine, humidityRate[i].yLine, '--', color=otherColors[i])
            axs[2].set_title("Relative Humidity (%RH)")
            axs[2].set_xlabel("Time (s)")
            axs[2].set_ylabel("%RH")
            axs[2].legend()
            # Plot rate of change of relative humidity in subplot 3

            if numSubPlots == 4:
                for i in range(len(humList)):
                    axs[3].plot(humidityRate[i].xLine, humidityRate[i].yPrime, label=pnames[i], color=colors[i])
                axs[3].set_title("%RH Rate of Change")
                axs[3].set_xlabel("Time (s)")
                axs[3].set_ylabel("Δ(%RH)")
                axs[3].legend()

            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.35)

            # Show the plot
            plt.show()

        except Exception as e: 
            print(e)
            print("Could not create plot")
            sys.exit(2)
    elif type == "mag":
        timeList = []
        xList = []
        yList = []
        zList = []
        colors = ["b","g","r","c","m","y","k"]
        for i in data:
            timeList.append(i.time)
            xList.append(i.x)
            yList.append(i.y)
            zList.append(i.z)
        # Create a subplot for each sensor
        j = 0
        try:
            plt.plot(timeList[j], xList[j], label="x", color=colors[0])
            plt.plot(timeList[j], yList[j], label="y", color=colors[1])
            plt.plot(timeList[j], zList[j], label="z", color=colors[2])
            # Show the plot
            plt.show()
        except:
            print("Could not create plot")
            sys.exit(2)

            

if __name__ == "__main__":
    main(sys.argv[1:])