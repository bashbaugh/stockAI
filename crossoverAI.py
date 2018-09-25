print("Importing modules...")
import pandas as pd
import config as cfg
import matplotlib.pyplot as plt
from time import sleep
import utils
print("done.")

DATA_FILE = "data/5minAAOI.csv"
sampleAt = 'close'
fastavgsamples = 3
slowavgsamples = 10
shares = 5
startmoney = 1000
money = startmoney

slowavglist, fastavglist = [],[]

csvdata = pd.read_csv(DATA_FILE)
print("Data loaded.")

def generateDataPoints(data):
    y = []
    for i in range(len(data[sampleAt])):
        y.append(data[sampleAt][i])
    return y

def generateAvg(data, position, numSamples):
    dsum = 0
    for i in range(-numSamples+1, 1):
        dsum += data[position + i]
    return dsum / numSamples

def calculate():
    fastavgrelpos = None # relative to slowavg
    oldfarelpos = None
    d = csvdata[sampleAt]
    for i in range(slowavgsamples):
        slowavglist.append(None)
        fastavglist.append(None)
    for i in range(slowavgsamples, len(d)):
        fastavg = generateAvg(d, i, fastavgsamples)
        slowavg = generateAvg(d, i, slowavgsamples)
        slowavglist.append(slowavg)
        fastavglist.append(fastavg)
        if fastavgrelpos != None:
            fastavgrelpos = 1 if slowavg <= fastavg else 0
            if oldfarelpos != fastavgrelpos:
                if fastavgrelpos == 1:
                    buy(d, i)
                else:
                    sell(d, i)
            oldfarelpos = fastavgrelpos
        else:
            fastavgrelpos = 1 if slowavg <= fastavg else 0
            oldfarelpos = fastavgrelpos
        
def buy(data, position):
    global money
    print("bought {0} shares at ${1}".format(shares, data[position]))
    money -= shares * data[position]
    
def sell(data, position):
    global money
    print("sold {0} shares at ${1}".format(shares, data[position]))
    money += shares * data[position]
        
print("Calculating")
calculate()


print("generating graph")
datapoints = generateDataPoints(csvdata)
plt.plot(datapoints, label='close')
plt.plot(slowavglist, label='slow average')
plt.plot(fastavglist, label='fast average')
plt.legend()

print("Profit: ${0}".format(money - startmoney))
print("showing graph")
sleep(1)
plt.show()
print("Goodbye.")


