
#!/usr/bin/python3
from pickle import FALSE, TRUE
import sys
import getopt
import matplotlib.pyplot as plt 

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

def printArgHelp():
    print("streamPlotter.py USAGE:")
    print("--type=<mag, atmo>")
    print("--file=<path to file>")

def main(argv):
    ## Check the args
    if len(argv) < 1:
        printArgHelp()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "-h",["type=","file="])
    except getopt.GetoptError:
        printArgHelp()
        sys.exit(2)

    # Parse the args
    type = "mag"
    compare = False
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
            if len(f) > 1:
                compare = True
            for i in f:
                files.append(i)

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
                data[k].setRecord(float(field[0]), float(field[1]), float(field[2]), float(field[3]))
            
            k += 1
    except:
        print("Error reading file: " + i)
        sys.exit(2)

    # Make some plots
    if type == "atmo":
        timeList = []
        tempList = []
        pressList = []
        humList = []
        pnames = []
        colors = ["b","g","r","c","m","y","k"]
        j = 0
        for i in data:
            timeList.append(i.time)
            tempList.append(i.x)
            pressList.append(i.y)
            humList.append(i.z)
            pnames.append("Atmo " + str(j))

            print("temperature range: " + str(min(tempList[j])) + " to " + str(max(tempList[j])))
            print("pressure range: " + str(min(pressList[j])) + " to " + str(max(pressList[j])))
            print("relative humidity range: " + str(min(humList[j])) + " to " + str(max(humList[j])))
            j += 1
        # Create a subplot for each sensor
        try:
            # Create a figure with three subplots
            fig, axs = plt.subplots(3, 1)
            # Name the figure
            fig.suptitle("Atmospheric Data")
            # Plot temperature in subplot 0
            for i in range(len(tempList)):
                axs[0].plot(timeList[i], tempList[i], label=pnames[i], color=colors[i])
            axs[0].set_title("Temperature (C)")
            axs[0].set_xlabel("Time (s)")
            axs[0].set_ylabel("°C")
            axs[0].legend()
            # Plot pressure in subplot 1
            for i in range(len(pressList)):
                axs[1].plot(timeList[i], pressList[i], label=pnames[i], color=colors[i])
            axs[1].set_title("Pressure (KPa)")
            axs[1].set_xlabel("Time (s)")
            axs[1].set_ylabel("KPa")
            axs[1].legend()
            # Plot relative humidity in subplot 2
            for i in range(len(humList)):
                axs[2].plot(timeList[i], humList[i], label=pnames[i], color=colors[i])
            axs[2].set_title("Relative Humidity (%RH)")
            axs[2].set_xlabel("Time (s)")
            axs[2].set_ylabel("%RH")
            axs[2].legend()
            # Show the plot
            plt.show()
        except:
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