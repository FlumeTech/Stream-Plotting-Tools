from tabulate import tabulate
import matplotlib.pyplot as plt
import humidityTesting as ht

# Print the atmospheric data in a table
def printAtmoData(atmo, label):
    # Get the min, max, and average values of the atmospheric data
    atmoRange = ht.atmoRanges()
    atmoRange.temperatureMin, atmoRange.temperatureMax, atmoRange.temperatureAvg = ht.getMinMaxMavg(atmo.x)
    atmoRange.humidityMin, atmoRange.humidityMax, atmoRange.humidityAvg = ht.getMinMaxMavg(atmo.z)
    atmoRange.pressureMin, atmoRange.pressureMax, atmoRange.pressureAvg = ht.getMinMaxMavg(atmo.y)

    # Print the atmospheric data in a table
    print(tabulate([["Temperature (C)", atmoRange.temperatureMin, atmoRange.temperatureAvg, atmoRange.temperatureMax],
                    ["Humidity (%RH)", atmoRange.humidityMin, atmoRange.humidityAvg, atmoRange.humidityMax],
                    ["Pressure (kPa)", atmoRange.pressureMin, atmoRange.pressureAvg, atmoRange.pressureMax]],
                     headers=[label, "Min", "Avg", "Max"], tablefmt="pipe"))
    print("\n")

# Print the humidity curve fit data in a table
def printFitData(fit, label):
    # Print the humidity curve fit data in a table
    print(tabulate([["Fit type", fit.fitType],["RMSE", fit.rmse],["A", fit.aCoeff],["B", fit.bCoeff]],
    headers=[label + " fit", "Value"], tablefmt="pipe"))
    print("\n")

# Present the atmospheric raw data and fit data in a plot and prints the data in a table
def presentFixedTempAndHumData(atmoList, fitList, labels ):
    # Print the min and max data to a table
    for i in range(len(atmoList)):
        printAtmoData(atmoList[i], labels[i])
        printFitData(fitList[i], labels[i])
    
    colors = ["b","g","r","c","m","y","k","#ccccff","#ff33cc","#336699","#888844","#cc6600","#000066"]

    # Create a figure with three subplots
    fig, axs = plt.subplots(3, 1)

    # Name the figure
    fig.suptitle("Atmospheric Data")

    # Plot temperature in subplot 0
    for i in range(len(atmoList)):
        axs[0].scatter(atmoList[i].time, atmoList[i].x, label=labels[i], color=colors[i])
    axs[0].set_title("Temperature (C)")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("°C")
    axs[0].legend()

    # Plot pressure in subplot 1
    for i in range(len(atmoList)):
        axs[1].scatter(atmoList[i].time, atmoList[i].y, label=labels[i], color=colors[i])
    axs[1].set_title("Pressure (KPa)")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("KPa")
    axs[1].legend()
    
    # Plot relative humidity and the curve fit in subplot 2
    for i in range(len(atmoList)):
        axs[2].scatter(atmoList[i].time, atmoList[i].z, label=labels[i], color=colors[i])
        axs[2].plot(fitList[i].time, fitList[i].fit, '--', label=(labels[i] + " fit"), color=colors[i])
    axs[2].set_title("Relative Humidity (%RH)")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("%RH")
    axs[2].legend()

    # Adjust the sublot spacing
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.35)

    # Show the plot
    plt.show()

# Present raw atmospheric data
def presentRawAtmoData(atmoList, labels):
    # Print the atmo min, max values
    for i in atmoList:
        printAtmoData(i, labels[atmoList.index(i)])

    colors = ["b","g","r","c","m","y","k","#ccccff","#ff33cc","#336699","#888844","#cc6600","#000066"]

    # Create a figure with three subplots
    fig, axs = plt.subplots(3, 1)

    # Name the figure
    fig.suptitle("Atmospheric Data")

    # Plot temperature in subplot 0
    for i in range(len(atmoList)):
        axs[0].scatter(atmoList[i].time, atmoList[i].x, label=labels[i], color=colors[i])
    axs[0].set_title("Temperature (C)")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("°C")
    axs[0].legend()

    # Plot pressure in subplot 1
    for i in range(len(atmoList)):
        axs[1].scatter(atmoList[i].time, atmoList[i].y, label=labels[i], color=colors[i])
    axs[1].set_title("Pressure (KPa)")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("KPa")
    axs[1].legend()

    # Plot relative humidity in subplot 2
    for i in range(len(atmoList)):
        axs[2].scatter(atmoList[i].time, atmoList[i].z, label=labels[i], color=colors[i])
    axs[2].set_title("Relative Humidity (%RH)")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("%RH")
    axs[2].legend()

    # Adjust the sublot spacing
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.35)

    # Show the plot
    plt.show()

# Present raw magnetometer data
def presentRawMagData(magData):
    # Make the plots
    for i in range(len(magData)):
        plt.plot(magData[i].time, magData[i].x, label="x", color="b")
        plt.plot(magData[i].time, magData[i].y, label="y", color="g")
        plt.plot(magData[i].time, magData[i].z, label="z", color="r")
    
    # Show the plot
    plt.show()

# Helper function for ranking rh data
def helper_func(ele):
        _, val, _ = ele.split()
        return float(val)

def presentRHComparison(atmoList, fitList, labels ):
    # Print the min and max data to a table
    for i in atmoList:
        printAtmoData(i, labels[atmoList.index(i)])
        printFitData(fitList[atmoList.index(i)], labels[atmoList.index(i)])
    
    colors = ["b","g","r","c","m","y","k","#ccccff","#ff33cc","#336699","#888844","#cc6600","#000066"]

    # Create a list for comparing the relative humidity rates
    rhComparison = []

    # Create a figure with one subplots
    fig, axs = plt.subplots(2, 1)

    # Name the figure
    fig.suptitle("Relative Humidity Comparison")

    # Plot relative humidity and the curve fit in subplot 0
    for i in range(len(atmoList)):
        axs[0].scatter(atmoList[i].time, atmoList[i].z, label=labels[i], color=colors[i])
        axs[0].plot(fitList[i].time, fitList[i].fit, '--', label=(labels[i] + " fit"), color=colors[i])
        rhComparison.append(labels[i] + " " + str(fitList[i].bCoeff) + " " + str(fitList[i].rmse))
    axs[0].set_title("Relative Humidity (%RH)")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("%RH")
    axs[0].legend()

    # Plot the slope in subplot 1
    for i in range(len(fitList)):
        axs[1].plot(fitList[i].time, fitList[i].fitPrime, label=labels[i] + " slope", color=colors[i])
    axs[1].set_title("Slope")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("Slope")
    axs[1].legend()

    # Create a table of rankings, sort from lowest to highest
    rhComparison.sort(key = helper_func)
    compData = []
    pp = 0
    for i in rhComparison:
        pp += 1
        bp = i.split()
        bp.append(str(pp))
        compData.append(bp)
    print (tabulate(compData, headers=["seal", "B Coeff", "r2", "rank"], tablefmt="pipe"))

    # Adjust the sublot spacing
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.35)

    # Show the plot
    plt.show()