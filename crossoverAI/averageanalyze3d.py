print("Importing modules...")
import pandas as pd
#import config as cfg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import sleep
import numpy as np
#import utils

print("done.")

DATA_FILE = "data/60minAAOI.csv"
sampleAt = 'close'
shares = 5
startmoney = 1000

slowavg_start = 1
fastavg_start = 1
slowavg_stop = 10
fastavg_stop = 10
slowavg_interval = 5
fastavg_interval = 5

X, Y, Z = [], [], []
bmoney, marketpos, prevtradeval, tradeprofits = None, None, None, None

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

def calculate(slowavgsamples, fastavgsamples):
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
            
def generate3d():
    profits = []
    for sa in range(slowavg_start, slowavg_stop, slowavg_interval):
        for fa in range(fastavg_start, fastavg_stop, fastavg_interval):
            slowavgsamples = sa
            fastavgsamples = fa
            global bmoney, marketpos, prevtradeval, tradeprofits
            slowavglist, fastavglist = [],[]
            bmoney = startmoney
            marketpos = 0
            tradeprofits = []
            prevtradeval = None
            fastavgrelpos = None # relative to slowavg
            oldfarelpos = None
            d = csvdata[sampleAt]
            for i in range(50):
                slowavglist.append(None)
                fastavglist.append(None)
            for i in range(50, len(d)):
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
                    oldfarelpos = fastavgrelpos
                else:
                    fastavgrelpos = 1 if slowavg <= fastavg else 0
                    oldfarelpos = fastavgrelpos
            nss_profit = (bmoney - startmoney)
            ss_profit = sum(tradeprofits)
            X.append(sa)
            Y.append(fa)
            Z.append(ss_profit)
            
    #slowavglist, fastavglist, tradepoints = [],[],[]
    #bmoney = startmoney
    #marketpos = 0
    #tradeprofits = []
    #prevtradeval = None
    #Calculate()
    #nss_profit = (bmoney - startmoney))
    #ss_profit = sum(tradeprofits)
    
        
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
generate3d()
X = np.asarray(X)
Y = np.asarray(Y)
Z = np.asarray(Z).reshape(1, 4)
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z,
                       linewidth=0, antialiased=False)


#print("showing graph")
#sleep(2)
plt.show()
#print("Goodbye.")


