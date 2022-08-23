# Base stream data class for storing stream logs
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