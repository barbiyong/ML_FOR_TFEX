import time
import requests
import re
import os
import pandas as pd
from talib_wrapper import *
from bokeh.plotting import figure, output_file, show

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


def get_y_long(data, period, delim, cutloss):
    slice = 500
    cutloss = cutloss * -1
    data = [float(i) for i in data]
    ret_list = []

    for i, item in enumerate(data):
        s = i + 1
        appnd = 0
        for k, j in enumerate(data[s:s + period]):
            ret = j - item
            if ret > delim:
                appnd = 1
                break
            elif ret < cutloss:
                appnd = 0
                break
        ret_list.append(appnd)

    # count = 0
    # for i in ret_list:
    #     if i == 1:
    #         count = count + 1
    # print('range:', period, count, len(ret_list), round(count / len(ret_list) * 100,2))

    # # train plott
    # # os.remove('train_data.html')
    # output_file("train_data.html", title='train_data_'+str(period)+'_'+str(delim))
    # p_data = data[slice:10000]
    # is_up = []
    # value = []
    #
    # for i, item in enumerate(ret_list[slice:10000]):
    #     if item == 1:
    #         is_up.append(i)
    #         value.append(p_data[i])
    #
    # p = figure(plot_width=1500, plot_height=800, x_axis_label='train_data')
    # p.line([i for i in range(int(len(p_data)))], p_data, line_width=1.5, color='grey')
    # p.circle(is_up, value, fill_color="blue", size=5)
    # # show(p)
    #
    # ##test plott
    # # os.remove('test_data.html')
    # output_file("test_data.html", title='test_data')
    # p_data = data[slice + 10000:]
    # is_up = []
    # value = []
    #
    # for i, item in enumerate(ret_list[slice + 10000:]):
    #     if item == 1:
    #         is_up.append(i)
    #         value.append(p_data[i])
    #
    # p = figure(plot_width=1500, plot_height=800, x_axis_label='test_data')
    # p.line([i for i in range(int(len(p_data)))], p_data, line_width=1.5, color='grey')
    # p.circle(is_up, value, fill_color="blue", size=5)
    # show(p)

    df = pd.DataFrame({'CLASS': ret_list[slice:]})

    return df


def get_x(ohlc):
    slice = 500
    EMA5 = get_ema(closes=ohlc[2], period=5)
    EMA10 = get_ema(closes=ohlc[2], period=10)
    EMA25 = get_ema(closes=ohlc[2], period=25)
    EMA50 = get_ema(closes=ohlc[2], period=50)
    EMA75 = get_ema(closes=ohlc[2], period=75)
    EMA200 = get_ema(closes=ohlc[2], period=200)
    RSI7 = get_rsi_7(closes=ohlc[2])
    ADX = get_adx(high=ohlc[3], low=ohlc[4], closes=ohlc[2])
    PDI = get_pdi(high=ohlc[3], low=ohlc[4], closes=ohlc[2])
    NDI = get_ndi(high=ohlc[3], low=ohlc[4], closes=ohlc[2])
    MACD, SIGNAL, HIST = get_macd(closes=ohlc[2])
    UBB, MBB, LBB = get_bbands(closes=ohlc[2])
    df = pd.DataFrame(
        {'UBB': UBB[slice:], 'CLOSE': ohlc[2][slice:], 'MBB': MBB[slice:], 'LBB': LBB[slice:], 'EMA5': EMA5[slice:], 'EMA10': EMA10[slice:], 'EMA25': EMA25[slice:],
         'EMA50': EMA50[slice:], 'EMA75': EMA75[slice:], 'EMA200': EMA200[slice:], 'RSI7': RSI7[slice:], 'MACD': MACD[slice:], 'HIST': HIST[slice:], 'PDI': PDI[slice:], 'NDI': NDI[slice:], 'ADX': ADX[slice:]})

    return df
