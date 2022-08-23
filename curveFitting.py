import numpy as np
from scipy.optimize import curve_fit


# Logarithmic function modeling the rise in relative humidity
def logarithmic(x, a, b):
    return a + b * np.log(x)


# Derivative of the logarithmic function
def dxLogarithmic(x, b):
    return b / x


# Find the x intercept of the logarithmic function
def findLogarithmicXIntercept(step, a, b):
    x = step
    y = logarithmic(x, a, b)
    while y < 0.0:
        x = x + step
        y = logarithmic(x, a, b)
    return x


# Find the y ending point so we can get the x - range
def findLogarithmicYEnd(step, a, b, yEnd, xMax=250000.0):
    x = step
    y = logarithmic(x, a, b)
    while y < yEnd and x < xMax:
        x = x + step
        y = logarithmic(x, a, b)
    return x


# Attempt to fit the logarithmic function to the dataset
def logarithmicCurveFit(x, y):
    # Fit the set, and get the constants
    popt, _ = curve_fit(logarithmic, x, y)
    a, b = popt

    # Set the steps size, then find the x range we wish to plot over
    dx = x[1] - x[0]
    xStart = findLogarithmicXIntercept(dx, a, b)
    xEnd = findLogarithmicYEnd(dx, a, b, 50.0)

    # Create the x - range
    xRange = np.arange(xStart, xEnd, dx)

    # Create the fitted curve
    logFit = logarithmic(xRange, a, b)

    # Create the derivative curve
    logPrimeFit = dxLogarithmic(xRange, b)

    # Calculate the root mean square error
    meanSquareError = np.mean((y - logarithmic(x, *popt))**2)
    residualError = np.dot((y - logarithmic(x, *popt)),
                           (y - logarithmic(x, *popt)))
    ymean = np.mean(y)
    errorTotal = np.dot((y - ymean), (y - ymean))
    r2 = 1 - residualError / errorTotal

    # Print the results
    print("Logarithmic Fit Results:")
    print("a = ", a)
    print("b = ", b)
    print("Root Mean Square Error = ", r2)
    print("X intercept = ", xStart)
    print("Upper boundary point = ", xEnd)

    # Return the xRange, the fitted curve, the derivative curve, the constants, rms value, and fit type
    return xRange, logFit, logPrimeFit, a, b, r2, "Logarithmic"