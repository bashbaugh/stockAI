import urllib.request
import os

AV_API_KEY = "YRHHBSGXRUKTR1KR"

path = os.path.dirname(os.path.abspath(__file__))

output_file = input("Please specify an output file:")
symbol = input("Specify a symbol:")
interval = input("Please specify an interval:") or "15min"
function = "TIME_SERIES_INTRADAY"
size = "full"
datatype = "csv"
apikey = AV_API_KEY

url = "https://www.alphavantage.co/query?symbol={0}&function={1}&interval={2}&outputsize={3}&datatype={4}&apikey={5}".format(symbol, function, interval, size, datatype, apikey)

print("\nfetching data from\n")
print(url + "\n")

urllib.request.urlretrieve(url, path + "/../data/" + output_file)

print("saved to {0}".format(str(output_file)))
