
#!/usr/bin/python3
from pickle import FALSE, TRUE
import sys
import getopt
import matplotlib.pyplot as plt 

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
    fname = ""
    type = "mag"
    for opt, arg in opts:
        if opt == '-h':
            printArgHelp()
            sys.exit()
        elif opt in ("-r1", "--type"):
            type = arg
        elif opt in ("-r2", "--file"):
            fname = arg

    # Screen the types
    if type != "mag" and type != "atmo":
        print("Invalid type: " + type)
        sys.exit(2)
    
    # Read the file
    try:
        f = open(fname, "r")
        buf = f.read()
        f.close()  
    except:
        print("Could not open file: " + fname)
        sys.exit(2)

    if type == "atmo":
        time = []
        tempInDegC = []
        pressureInKPa = []
        relativeHumidity = []
        i = 0
        for line in buf.split("\n"):
            if i < 4:
                i += 1
                continue
            field = line.split(",")
            if len(field) < 4:
                continue
            time.append(float(field[0]))
            tempInDegC.append(float(field[1]))
            pressureInKPa.append(float(field[2]))
            relativeHumidity.append(float(field[3]))

        print("temperature range: " + str(min(tempInDegC)) + " to " + str(max(tempInDegC)))
        print("pressure range: " + str(min(pressureInKPa)) + " to " + str(max(pressureInKPa)))
        print("relative humidity range: " + str(min(relativeHumidity)) + " to " + str(max(relativeHumidity)))
        
        # Create a subplot for each sensor
        try:
            # Create a figure with three subplots
            fig, axs = plt.subplots(3, 1)
            # Name the figure
            fig.suptitle("Atmospheric Data")
            # Plot temperature in subplot 0
            axs[0].plot(time, tempInDegC, color="red")
            axs[0].set_title("Temperature (C)")
            axs[0].set_xlabel("Time (s)")
            axs[0].set_ylabel("°C")
            # Plot pressure in subplot 1
            axs[1].plot(time, pressureInKPa, color="blue")
            axs[1].set_title("Pressure (KPa)")
            axs[1].set_xlabel("Time (s)")
            axs[1].set_ylabel("KPa")
            # Plot relative humidity in subplot 2
            axs[2].plot(time, relativeHumidity, color="green")
            axs[2].set_title("Relative Humidity (%RH)")
            axs[2].set_xlabel("Time (s)")
            axs[2].set_ylabel("%RH")
            # Show the plot
            plt.show()
        except:
            print("Could not create plot")
            sys.exit(2)
            

if __name__ == "__main__":
    main(sys.argv[1:])