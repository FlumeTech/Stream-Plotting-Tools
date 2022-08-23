import streamData as sd
import curveFitting as cf


# Storage class for humidity curve fitting data
class humidityFit:
    time = []
    fit = []
    fitPrime = []
    aCoeff = 0.0
    bCoeff = 0.0
    rmse = 0.0
    fitType = "logarithmic"

    def __init__(self):
        self.time = []
        self.fit = []
        self.fitPrime = []
        self.aCoeff = 0.0
        self.bCoeff = 0.0
        self.rmse = 0.0
        self.fitType = "logarithmic"

    def setRecord(self, time, fit, fitP, a, b, rmse):
        self.time.append(time)
        self.fit.append(fit)
        self.fitPrime.append(fitP)
        self.aCoeff = a
        self.bCoeff = b
        self.rmse = rmse
        self.fitType = "logarithmic"


# Storage class for atmospheric data ranges
class atmoRanges:
    temperatureMin = 0.0
    temperatureAvg = 0.0
    temperatureMax = 0.0
    humidityMin = 0.0
    humidityAvg = 0.0
    humidityMax = 0.0
    pressureMin = 0.0
    pressureAvg = 0.0
    pressureMax = 0.0

    def __init__(self):
        self.temperatureMin = 0.0
        self.temperatureAvg = 0.0
        self.temperatureMax = 0.0
        self.humidityMin = 0.0
        self.humidityAvg = 0.0
        self.humidityMax = 0.0
        self.pressureMin = 0.0
        self.pressureAvg = 0.0
        self.pressureMax = 0.0


# Get the min, the max, and the average values of a series
def getMinMaxMavg(series):
    mn = min(series)
    mx = max(series)
    avg = sum(series) / len(series)
    return mn, mx, avg


# Find the start of the stable temperature and humidity period
def findStableLowTemp(time, temp, minStablePeriod=3000):
    print("Finding stable low temperature..")

    # Configure the low index, temperature, and start time
    lowIndex = 0
    low = temp[lowIndex]
    startTime = time[0]

    # Loop through the temperature data, once we find a stable period for minStablePeriod return the low index
    for i in range(len(temp)):
        if temp[i] == low:
            delta = time[i] - startTime
            if delta > minStablePeriod:
                lowIndex = i
                break
        elif temp[i] < low:
            startTime = time[i]
            low = temp[i]

    print("Low temperature of " + str(low) + " found at index " +
          str(lowIndex))
    return lowIndex


# Top level function for testing humidity data from the fixed temperature and humidity chamber
def fixedTempAndHumidityProcess(series):
    print("Fixed temperature and humidity chamber data processing..")

    # Clip the data so we only examine the stable temperature and humidity period
    lowIndex = findStableLowTemp(series.time, series.x)
    clippedSeries = sd.streamData()
    clippedSeries.time = series.time[lowIndex:]
    clippedSeries.x = series.x[lowIndex:]
    clippedSeries.y = series.y[lowIndex:]
    clippedSeries.z = series.z[lowIndex:]

    # Create the humidity curve fitting data
    humidityFitData = humidityFit()
    humidityFitData.time, humidityFitData.fit, humidityFitData.fitPrime, humidityFitData.aCoeff, humidityFitData.bCoeff, humidityFitData.rmse, humidityFitData.fitType = cf.logarithmicCurveFit(
        clippedSeries.time, clippedSeries.z)

    return clippedSeries, humidityFitData