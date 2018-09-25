print("Importing modules...")
import pandas as pd
#import config as cfg
import matplotlib.pyplot as plt
from time import sleep
#import utils

print("done.")

DATA_FILE = "data/60minAAOI.csv"
sampleAt = 'close'
fastavgsamples = 15
slowavgsamples = 20
shares = 5
startmoney = 1000
money = startmoney

slowavglist, fastavglist = [],[]
previoustradeval = None
tradeprofits = []

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
    global money, previoustradeval, tradeprofits
    print("bought {0} shares at ${1}".format(shares, data[position]))
    money -= shares * data[position]
    if previoustradeval != None:
        tradeprofits.append(previoustradeval - data[position])
        print("profit: " + str(previoustradeval - data[position]) + "\n")
    previoustradeval = data[position]
    
def sell(data, position):
    global money, previoustradeval, tradeprofits
    print("sold {0} shares at ${1}".format(shares, data[position]))
    money += shares * data[position]
    if previoustradeval != None:
        tradeprofits.append(data[position] - previoustradeval)
        print("profit: " + str(data[position] - previoustradeval) + "\n")
    previoustradeval = data[position]
        
print("Calculating")
calculate()


print("generating graph")
datapoints = generateDataPoints(csvdata)
plt.plot(datapoints, label='close')
plt.plot(slowavglist, label='slow average')
plt.plot(fastavglist, label='fast average')
plt.legend()

print("Profit: ${0}".format(money - startmoney))
print("Profit m2: ${0}".format(sum(tradeprofits)))
print("showing graph")
sleep(2)
plt.show()
print("Goodbye.")


