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

slowavglist, fastavglist, tradepoints = [],[],[]
bmoney = startmoney
marketpos = 0
tradeprofits = []
prevtradeval = None

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
                    trade(1, d, i)
                else:
                    trade(-1, d, i) 
                tradepoints.append(i)
            oldfarelpos = fastavgrelpos
        else:
            fastavgrelpos = 1 if slowavg <= fastavg else 0
            oldfarelpos = fastavgrelpos
        
def trade(takeposition, data, index):
    global bmoney, prevtradeval, marketpos, tradeprofits
    if takeposition == 1:
        bmoney -= shares * data[index]
        print("\nbought {0} shares at ${1}".format(shares, data[index]))
        if marketpos != 0:
            profit = (prevtradeval - data[index])
            tradeprofits.append(profit)
            print("Bought long, profit was:\n{0}".format(profit))
        marketpos = 1
        prevtradeval = data[index]
    else:
        bmoney += shares * data[index]
        print("\nsold {0} shares at ${1}".format(shares, data[index]))
        if marketpos != 0:
            profit = (prevtradeval - data[index]) * -1
            tradeprofits.append(profit)
            print("Sold short, profit was:\n{0}".format(profit))
        marketpos = -1
        prevtradeval = data[index]
    
    
#def sellshort(position, data, index):
    #global money
    #print("sold {0} shares at ${1}".format(shares, data[index]))
    #money += shares * data[index]
    
print("Calculating")
calculate()


print("\n\ngenerating graph")
datapoints = generateDataPoints(csvdata)
plt.plot(datapoints, marker='*',label='close', markevery=tradepoints,  markersize=10)
plt.plot(slowavglist, label='slow average')
plt.plot(fastavglist, label='fast average')
plt.legend()

print("Profit without short-selling: ${0}".format(bmoney - startmoney))
finalprofit = sum(tradeprofits)
print("Profit: ${0}".format(finalprofit))
print("showing graph")
sleep(2)
plt.show()
print("Goodbye.")


