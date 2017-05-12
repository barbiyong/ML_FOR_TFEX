# coding: utf-8

# In[1]:

import re
import time
import requests
import operator
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

from bokeh.plotting import figure, output_file, show

import warnings

warnings.filterwarnings("ignore")


# In[2]:

# Exponential Moving Average
def EMA(df, n):
    EMA = pd.Series(pd.ewma(df['Close'], span=n, min_periods=n - 1), name='EMA_' + str(n))
    df = df.join(EMA)
    return df


# Momentum
def MOM(df, n):
    M = pd.Series(df['Close'].diff(n), name='Momentum_' + str(n))
    df = df.join(M)
    return df


# Rate of Change
def ROC(df, n):
    M = df['Close'].diff(n - 1)
    N = df['Close'].shift(n - 1)
    ROC = pd.Series(M / N, name='ROC_' + str(n))
    df = df.join(ROC)
    return df


# Average True Range
def ATR(df, n):
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.get_value(i + 1, 'High'), df.get_value(i, 'Close')) - min(df.get_value(i + 1, 'Low'),
                                                                              df.get_value(i, 'Close'))
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(pd.ewma(TR_s, span=n, min_periods=n), name='ATR_' + str(n))
    df = df.join(ATR)
    return df


# Bollinger Bands
def BBANDS(df, n):
    MA = pd.Series(pd.rolling_mean(df['Close'], n))
    MSD = pd.Series(pd.rolling_std(df['Close'], n))
    b1 = 4 * MSD / MA
    B1 = pd.Series(b1, name='BollingerB_' + str(n))
    df = df.join(B1)
    b2 = (df['Close'] - MA + 2 * MSD) / (4 * MSD)
    B2 = pd.Series(b2, name='Bollinger%b_' + str(n))
    df = df.join(B2)
    return df


# Stochastic oscillator %K
def STOK(df):
    SOk = pd.Series((df['Close'] - df['Low']) / (df['High'] - df['Low']), name='SO%k')
    df = df.join(SOk)
    return df


# Stochastic oscillator %D
def STO(df, n):
    SOk = pd.Series((df['Close'] - df['Low']) / (df['High'] - df['Low']), name='SO%k')
    SOd = pd.Series(pd.ewma(SOk, span=n, min_periods=n - 1), name='SO%d_' + str(n))
    df = df.join(SOd)
    return df


# Average Directional Movement Index
def ADX(df, n, n_ADX):
    i = 0
    UpI = []
    DoI = []
    while i + 1 <= df.index[-1]:
        UpMove = df.get_value(i + 1, 'High') - df.get_value(i, 'High')
        DoMove = df.get_value(i, 'Low') - df.get_value(i + 1, 'Low')
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.get_value(i + 1, 'High'), df.get_value(i, 'Close')) - min(df.get_value(i + 1, 'Low'),
                                                                              df.get_value(i, 'Close'))
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(pd.ewma(TR_s, span=n, min_periods=n))
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(pd.ewma(UpI, span=n, min_periods=n - 1) / ATR)
    NegDI = pd.Series(pd.ewma(DoI, span=n, min_periods=n - 1) / ATR)
    ADX = pd.Series(pd.ewma(abs(PosDI - NegDI) / (PosDI + NegDI), span=n_ADX, min_periods=n_ADX - 1),
                    name='ADX_' + str(n) + '_' + str(n_ADX))
    df = df.join(ADX)
    return df


# MACD, MACD Signal and MACD difference
def MACD(df, n_fast, n_slow):
    EMAfast = pd.Series(pd.ewma(df['Close'], span=n_fast, min_periods=n_slow - 1))
    EMAslow = pd.Series(pd.ewma(df['Close'], span=n_slow, min_periods=n_slow - 1))
    MACD = pd.Series(EMAfast - EMAslow, name='MACD_' + str(n_fast) + '_' + str(n_slow))
    MACDsign = pd.Series(pd.ewma(MACD, span=9, min_periods=8), name='MACDsign_' + str(n_fast) + '_' + str(n_slow))
    MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff_' + str(n_fast) + '_' + str(n_slow))
    df = df.join(MACD)
    df = df.join(MACDsign)
    df = df.join(MACDdiff)
    return df


# Relative Strength Index
def RSI(df, n):
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= df.index[-1]:
        UpMove = df.get_value(i + 1, 'High') - df.get_value(i, 'High')
        DoMove = df.get_value(i, 'Low') - df.get_value(i + 1, 'Low')
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(pd.ewma(UpI, span=n, min_periods=n - 1))
    NegDI = pd.Series(pd.ewma(DoI, span=n, min_periods=n - 1))
    RSI = pd.Series(PosDI / (PosDI + NegDI), name='RSI_' + str(n))
    df = df.join(RSI)
    return df


# In[3]:

def get_ohlc(stockName, period):
    # by Yortz Smile!!!!
    dataList = {}
    url = "http://ws.efinancethai.com/smartws/service.asmx"
    # headers = {'content-type': 'application/soap+xml'}
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; MS Web Services Client Protocol 4.0.30319.42000)', 'Content-Type': 'text/xml; charset=utf-8',
               'SOAPAction': '"http://10.88.40.3/webservices/ReturnValue"', 'Host': 'ws.efinancethai.com', 'Content-Length': '487', 'Expect': '100-continue', 'Connection': 'close'}
    body = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ReturnValue xmlns="http://10.88.40.3/webservices/"><Key>01-bls50487</Key><Cmd>007</Cmd><Param>' + stockName + '|1968-12-12|' + time.strftime(
        '%Y-%m-%d') + '|' + period + '|||2.0|0|True|False|False|False|False|False|False|1||||False||False|0|False|False|12|False|False</Param></ReturnValue></soap:Body></soap:Envelope>'
    response = requests.post(url, data=body, headers=headers)
    data = re.search('<ReturnValueResult>(.*)</ReturnValueResult>', str(response.content)).group(1).split('|')[:-1]
    Date = []
    Close = []
    Open = []
    Low = []
    High = []
    for row in data:
        Date.append(row.split(',')[0])
        Open.append(float(row.split(',')[1]))
        High.append(float(row.split(',')[2]))
        Low.append(float(row.split(',')[3]))
        Close.append(float(row.split(',')[4]))

    return Date, Open, Close, High, Low


# In[70]:

def plot_sampling(close, ret_list):
    print(close)
    colors = []
    index = []
    b_value = []
    trade_index = []
    for i, value in enumerate(ret_list):
        if value == 1:
            trade_index.append((i, 'green'))
        elif value == -1:
            trade_index.append((i, 'red'))
    for i, item in enumerate(trade_index):
        b_value.append(close[item[0]])
        index.append(item[0])
        colors.append(item[1])
    # os.remove('sampling.html')
    output_file("sampling.html", title='sampling plot')
    p = figure(plot_width=1080, plot_height=720, x_axis_label='sampling plot')
    p.line([i for i in range(int(len(close)))], close, line_width=1.5, color='grey')
    p.circle(index, b_value, color=colors, size=5)
    show(p)


# In[5]:

def fit_predict_RandomForestClassifier(X_train, Y, X_test):
    m = RandomForestClassifier(n_estimators=10)
    m.fit(X_train, Y.values.ravel())
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    filename = '000.sav'
    joblib.dump(m, filename)
    return y_train, y_test


# In[6]:

def short_cond(close, short_tp, short_cl, short_pe):
    ret_list = []
    for i, cls in enumerate(close):
        appnd = 0
        for next_close in close[i + 1:i + short_pe]:
            diff = float(cls) - float(next_close)
            if diff > short_tp:
                appnd = -1
                break
            elif diff < -short_cl:
                appnd = 0
                break
        ret_list.append(appnd)
    return ret_list


def long_cond(close, long_tp, long_cl, long_pe):
    ret_list = []
    for i, cls in enumerate(close):
        appnd = 0
        for next_close in close[i + 1:i + long_pe]:
            diff = next_close - cls
            if diff > long_tp:
                appnd = 1
                break
            elif diff < -long_cl:
                appnd = 0
                break
        ret_list.append(appnd)
    return ret_list


def get_y(ohlc, long_tp, long_cl, long_pe, short_tp, short_cl, short_pe):
    long_ret = long_cond(ohlc, long_tp, long_cl, long_pe)
    short_ret = short_cond(ohlc, short_tp, short_cl, short_pe)
    return long_ret, short_ret


# In[7]:

ohlc = get_ohlc('S50M17', '5')
print(len(ohlc[0]), len(ohlc[0][-65:]))

# In[8]:

long_tp = 3
long_cl = 1
long_pe = 50
short_tp = 3
short_cl = 1
short_pe = 50
slice = 500
train_window = int(len(ohlc[0]) * 0.8)

# In[71]:

y_long, y_short = get_y(ohlc[2], long_tp, long_cl, long_pe, short_tp, short_cl, short_pe)
plot_sampling(close=ohlc[2], ret_list=y_long)
plot_sampling(close=ohlc[2], ret_list=y_short)

y = pd.DataFrame({'CLASS': y_long[slice:]})
# y = pd.DataFrame({'CLASS': y_short[slice:]})
print(len(y))


# In[60]:

def get_x(ohlc, slice):
    df = pd.DataFrame({'Open': ohlc[1], 'Close': ohlc[2], 'High': ohlc[3], 'Low': ohlc[4]})
    df = EMA(df, 5)
    df = EMA(df, 10)
    df = EMA(df, 25)
    df = EMA(df, 50)
    df = EMA(df, 75)
    df = EMA(df, 200)
    df = RSI(df, 7)
    df = MACD(df=df, n_fast=12, n_slow=26)
    df = MOM(df, 14)
    df = ROC(df, 10)
    df = ATR(df, 14)
    df = BBANDS(df, 20)
    df = ADX(df, 14, 14)
    return df[slice:]


x = get_x(ohlc, slice)

x_train_raw = x[:train_window]
y_train_raw = y[:train_window]
x_test_raw = x[train_window:]
y_test_raw = y[train_window:]

train_acc = 0
test_acc = 0
loop_time = 10

for i in range(loop_time):
    y_train, y_test = fit_predict_RandomForestClassifier(x_train_raw, y_train_raw, x_test_raw)
    train_acc = train_acc + round(accuracy_score(y_train_raw, y_train), 3) * 100
    test_acc = test_acc + round(accuracy_score(y_test_raw, y_test), 3) * 100

print('train score:', train_acc / loop_time)
print('test_acc:', test_acc / loop_time)

# In[65]:

plot_sampling(ohlc[2][-y_test.size:], y_test.tolist())


# In[61]:



