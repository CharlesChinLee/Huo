from huobi import RequestClient
from huobi.model import *

request_client = RequestClient()


candlestick_list = request_client.get_latest_candlestick("btcusdt", CandlestickInterval.DAY1,10)
print("---- 1 min candlestick for btcusdt ----")
for item in candlestick_list:
    print("Timestamp: " + str(item.timestamp))
    print("High: " + str(item.high))
    print("Low: " + str(item.low))
    print("Open: " + str(item.open))
    print("Close: " + str(item.close))
    print("Volume: " + str(item.volume))
    print()
