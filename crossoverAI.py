print("Importing modules...")
import pandas as pd
import config as cfg
import matplotlib.pyplot as plt
import utils
print("done.")

DATA_FILE = "data/5minAAOI.csv"
fastavgsamples = 4
slowavgsamples = 12

csvdata = pd.read_csv(DATA_FILE)
print("Data loaded.")

def generateDataPoints(data, sampleAt):
    y = []
    for i in range(len(data[sampleAt])):
        y.append(data[sampleAt][i])
    return y





print("generating graph")
datapoints = generateDataPoints(csvdata, 'close')
plt.plot(datapoints)

print("showing graph")
plt.show()
print("Goodbye.")


