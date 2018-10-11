print("Importing modules...")
import pandas as pd
import config as cfg
import matplotlib.pyplot as plt
from collection import deque
import utils
print("done.")

DATA_FILE = "data/5minAAOI.csv"
sampleAt = 'close'
fastavgsamples = 20
slowavgsamples = 60

fastavgrelpos = 1 # relative to slowavg
slowavglist, fastavglist = [],[]
fastavgarray, slowavgarray = [],[]
currPos =slowavgsamples

csvdata = pd.read_csv(DATA_FILE)
print("Data loaded.")

def generateDataPoints(data):
    y = []
    for i in range(len(data[sampleAt])):
        y.append(data[sampleAt][i])
    return y

#def generateAvg(data, position, numSamples):
    #dsum = 0
    #for i in range(-numSamples+1, 1):
        #dsum += data[position + i]
    #return dsum / numSamples
    
def nextAvg(data, position, numSamples):
        dsum = 0
        for i in range(-numSamples+1, 1):
            dsum += data[position + i]
        return dsum / numSamples

def calculate():
    
    d = csvdata[sampleAt]
    for i in range(slowavgsamples):
        slowavglist.append(None)
        fastavglist.append(None)
    for i in range(slowavgsamples, len(d)):
        slowavglist.append(nextAvg(slowavgsamples))
        fastavglist.append(nextAvg(d, i, fastavgsamples))
        
print("Calculating")
calculate()

    
print("generating graph")
datapoints = generateDataPoints(csvdata)
plt.plot(datapoints, label='close')
plt.plot(slowavglist, label='slow average')
plt.plot(fastavglist, label='fast average')
plt.legend()

print("showing graph")
plt.show()
print("Goodbye.")


 
