import pandas as pd
import config
import urllib

#pd.DataFrame.from_csv('UBL.csv')

def APIfetchdata(symbol, interval="5min", function=\
    "TIME_SERIES_INTRADAY", size="full", datatype="csv", apikey=config.AV_API_KEY):
    
    print("fetching data from")
    
    url = "https://www.alphavantage.co/query?symbol={0}&function={1}&interval={2}&outputsize={3}&datatype={4}&apikey={5}".format(symbol, function, interval, size, datatype, apikey)
    
    print(url + "\n\n\n")
    
    #csv = urllib.request.urlopen(url).read()
    
    data = pd.read_csv("data/intraday_5min_AAOI.csv")
    
    print(data)
    

APIfetchdata("AAOI")
