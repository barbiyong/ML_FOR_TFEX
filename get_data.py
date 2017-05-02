import time
import requests
import re

def get_ohlc(stockName, period):
    # by Yortz Smile!!!!
    dataList = {}
    url = "http://ws.efinancethai.com/smartws/service.asmx"
    # headers = {'content-type': 'application/soap+xml'}
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; MS Web Services Client Protocol 4.0.30319.42000)', \
               'Content-Type': 'text/xml; charset=utf-8', \
               'SOAPAction': '"http://10.88.40.3/webservices/ReturnValue"', \
               'Host': 'ws.efinancethai.com', \
               'Content-Length': '487', \
               'Expect': '100-continue', \
               'Connection': 'close' \
               }
    body = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ReturnValue xmlns="http://10.88.40.3/webservices/"><Key>01-bls50487</Key><Cmd>007</Cmd><Param>' + stockName + '|1968-12-12|' + time.strftime(
        '%Y-%m-%d') + '|' + period + '|||2.0|0|True|False|False|False|False|False|False|1||||False||False|0|False|False|12|False|False</Param></ReturnValue></soap:Body></soap:Envelope>'
    response = requests.post(url, data=body, headers=headers)
    data = re.search('<ReturnValueResult>(.*)</ReturnValueResult>', str(response.content)).group(1).split('|')[:-1]
    Date = []
    Close = []
    Open = []
    Low = []
    # Volume = []
    High = []
    for row in data:
        Date.append(row.split(',')[0])
        Open.append(float(row.split(',')[1]))
        High.append(float(row.split(',')[2]))
        Low.append(float(row.split(',')[3]))
        Close.append(float(row.split(',')[4]))
        # Volume.append(float(row.split(',')[5]) * 100)

    return Date, Open, Close, High, Low

# data = get_ohlc('S50M17', '3')
# total = 0
# lenght = int(len(data[0]))
#
# for i in range(lenght-1000, lenght):
#     print(data[0][i])
#     diff = data[3][i] - data[4][i]
#     total = total + diff
# print('avg:', total/lenght)
