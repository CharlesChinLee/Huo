from huobi import RequestClient
from huobi.model import *
from huobi.exception.huobiapiexception import HuobiApiException
import json
import time
import os
from datetime import datetime

request_client = RequestClient()
exchange_info = request_client.get_exchange_info()
symbol_map = request_client.get_my_symbol_map()
base_symbol=['usdt','eth','btc']
for i in range(3):
    s_now = base_symbol[i]
    folder = './KlineData1day' + s_now
    if not os.path.exists(folder):
        os.makedirs(folder)
        print  (folder + ' created ')
    else:
        for ki in os.listdir(folder):
            path_file = os.path.join(folder, ki)
            if os.path.isfile(path_file):
                os.remove(path_file)
        print(folder + ' cleared ')
    for symbol in symbol_map[s_now]:
        time.sleep(0.1)
        print(symbol.symbol)
        try:
            candlestick_list = request_client.get_latest_candlestick(symbol.symbol, CandlestickInterval.DAY1, 30)
        except (HuobiApiException, json.JSONDecodeError):
            print('SomeThing Error')
        else:

            file_name = './KlineData1day'+s_now+'/' + symbol.symbol
            csv_file = open(file_name, 'w')
            for item in candlestick_list:
                # print("Timestamp: " + str(item.timestamp))
                # print("High: " + str(item.high))
                # print("Low: " + str(item.low))
                # print("Open: " + str(item.open))
                # print("Close: " + str(item.close))
                # print("Volume: " + str(item.volume))
                datestr = datetime.strftime(datetime.utcfromtimestamp(item.timestamp/1000 + 16 * 60 * 60), "%Y%m%d %H%M%S")
                csv_file.write(datestr + ' ' + str(item.open) + ' ' + str(item.high) + ' ' + str(item.low) +' '+ str(item.close) + '\t\n')
            csv_file.close()


