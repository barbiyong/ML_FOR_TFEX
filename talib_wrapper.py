import math
import talib
import numpy as np
from decimal import Decimal


def to_decimal_or_none(value):
    return value if not math.isnan(value) else None


def get_ema(closes, period: int):
    closes = np.array(closes, dtype=float)
    ema = talib.EMA(closes, timeperiod=period)
    return ema

def get_rsi_14(closes):
    closes = np.array(closes, dtype=float)
    rsi = talib.RSI(closes, timeperiod=14)

    return rsi


def get_rsi_7(closes):
    closes = np.array(closes, dtype=float)
    rsi = talib.RSI(closes, timeperiod=7)

    return rsi


def get_macd(closes):
    closes = np.array(closes, dtype=float)
    macd, macdsignal, macdhist = talib.MACD(np.array(closes, dtype=float), 12, 26, 9)
    return macd, macdsignal, macdhist


def macd_main(closes):
    # print(closes)
    macd, macdsignal, macdhist = talib.MACD(np.array(closes, dtype=float), 12, 26, 9)
    # print(macd, macdsignal)
    ret_val = macd
    # ret_val = ['%.2f' % i for i in ret_val]
    return ret_val


def macd_diff(closes):
    # print(closes)
    macd, macdsignal, macdhist = talib.MACD(np.array(closes, dtype=float), 12, 26, 9)
    # print(macd)
    # ret_val = ['%.2f' % i for i in ret_val]
    return macd/macdsignal


def macd_vs_signal(closes):
    macd = talib.MACDFIX(np.array(closes, dtype=float))
    ret_val = [x / y for x, y in zip(macd[0], macd[1])]
    ret_val = ['%.2f' % i for i in ret_val]
    return ret_val


def ismacdup(closes):
    closes = np.array(list(closes), dtype=float)
    macd = talib.MACDFIX(closes)
    # print(macd[0][-1], macd[1][-1])
    if macd[0][-1] > macd[1][-1]:
        ret_val = int(1)
    else:
        ret_val = int(0)

    return ret_val


def smav(stockData, point, timeRange):
    CONSTANT_LAST_ELEMENT = -1
    floatData = [float(x) for x in stockData['volume']]
    real = np.array(floatData[:point])
    smav = talib.SMA(real, timeperiod=timeRange)

    return (smav[CONSTANT_LAST_ELEMENT]);


def ema(stockData, point, timeRange):
    CONSTANT_LAST_ELEMENT = -1
    ema = talib.EMA(stockData['close'][:point], timeperiod=timeRange)

    return (ema[CONSTANT_LAST_ELEMENT]);



def compare2Value(firstValue, secondValue):
    return (firstValue / secondValue)


# DEMA - Double Exponential Moving Average
def dema(stockData, point):
    return talib.DEMA(stockData['close'][:point], timeperiod=30)[-1]


# HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
def hilbert(stockData, point):
    return talib.HT_TRENDLINE(stockData['close'][:point])[-1]


# KAMA - Kaufman Adaptive Moving Average
def kaufman(stockData, point, period):
    return talib.KAMA(stockData['close'][:point], timeperiod=period)[-1]


# MAMA - MESA Adaptive Moving Average
def mama_fama(stockData, point):
    mama_fama = talib.MAMA(stockData['close'][:point], fastlimit=0, slowlimit=0)
    mama = mama_fama[0]
    fama = mama_fama[1]
    return mama[-1], fama[-1]


def fama(stockData, point):
    return talib.MAMA(stockData['close'][:point], fastlimit=0, slowlimit=0)[1][-1]


# MIDPOINT - MidPoint over period
def mid_point(stockData, point):
    return talib.MIDPOINT(stockData['close'][:point], timeperiod=14)[-1]


# MIDPRICE - Midpoint Price over period
def mid_price(stockData, point):
    return talib.MIDPRICE(stockData['high'][:point], stockData['low'][:point], timeperiod=14)[-1]


# SAR - Parabolic SAR
def sar(stockData, point):
    return talib.SAR(stockData['high'][:point], stockData['low'][:point], acceleration=0, maximum=0)[-1]


''' _________________ Momentum Indicator Functions _________________ '''


# ADX - Average Directional Movement Index
def adx(stockData, point, period):
    return talib.ADX(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], timeperiod=period)[-1]


# ADXR - Average Directional Movement Index Rating
def adxr(stockData, point, period):
    return talib.ADXR(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point],
                      timeperiod=period)[-1]


# APO - Absolute Price Oscillator
def apo(stockData, point):
    return talib.APO(stockData['close'][:point], fastperiod=12, slowperiod=26, matype=0)[-1]


# AROON - Aroon
def aroon_up(stockData, point):
    return talib.AROON(stockData['high'][:point], stockData['low'][:point], timeperiod=14)[0][-1]


def aroon_down(stockData, point):
    return talib.AROON(stockData['high'][:point], stockData['low'][:point], timeperiod=14)[0][-1]


# AROONOSC - Aroon Oscillator
def aroon_osc(stockData, point):
    return talib.AROONOSC(stockData['high'][:point], stockData['low'][:point], timeperiod=14)[-1]


# BOP - Balance Of Power
def bop(stockData, point):
    return talib.BOP(stockData['open'][:point], stockData['high'][:point], stockData['low'][:point], stockData['close'][:point])[-1]


# CCI - Commodity Channel Index
def cci(stockData, point):
    return talib.CCI(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], timeperiod=14)[-1]


# CMO - Chande Momentum Oscillator
def cmo(stockData, point, period):
    return talib.CMO(stockData['close'][:point], timeperiod=period)[-1]


# DX - Directional Movement Index
def dx(stockData, point, period):
    return talib.DX(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], timeperiod=period)[-1]


# MACD - Moving Average Convergence/Divergence
def macd_hist(stockData, point):
    return talib.MACD(stockData['close'][:point], fastperiod=12, slowperiod=26, signalperiod=9)[2][-1]


# MFI - Money Flow Index
def mfi(stockData, point, period):
    volume = np.array(stockData['volume'][:point], dtype='d')
    return talib.MFI(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], volume,
                     timeperiod=period)[-1]


# MINUS_DI - Minus Directional Indicator
def minus_di(stockData, point, period):
    return talib.MINUS_DI(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point],
                          timeperiod=period)[-1]


# MINUS_DM - Minus Directional Movement
def minus_dm(stockData, point, period):
    return talib.MINUS_DM(stockData['high'][:point], stockData['low'][:point], timeperiod=period)[-1]


# MOM - Momentum
def momentum(stockData, point):
    return talib.MOM(stockData['close'][:point], timeperiod=10)[-1]


# PLUS_DI - Plus Directional Indicator
def plus_di(stockData, point, period):
    return talib.PLUS_DI(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point],
                         timeperiod=period)[-1]


# PLUS_DM - Plus Directional Movement
def plus_dm(stockData, point, period):
    return talib.PLUS_DM(stockData['high'][:point], stockData['low'][:point], timeperiod=period)[-1]


# PPO - Percentage Price Oscillator
def ppo(stockData, point):
    return talib.PPO(stockData['close'][:point], fastperiod=12, slowperiod=26, matype=0)[-1]


# ROC - Rate of change : ((price/prevPrice)-1)*100
def roc(stockData, point):
    return talib.ROC(stockData['close'][:point], timeperiod=10)[-1]


# ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
def rocp(stockData, point):
    return talib.ROCP(stockData['close'][:point], timeperiod=10)[-1]


# ROCR - Rate of change ratio: (price/prevPrice)
def rocr(stockData, point):
    return talib.ROCR(stockData['close'][:point], timeperiod=10)[-1]


# ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
def roc100(stockData, point):
    return talib.ROCR100(stockData['close'][:point], timeperiod=10)[-1]


# STOCH - Stochastic
def sto_slow_k(stockData, point):
    return \
        talib.STOCH(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], fastk_period=5,
                    slowk_period=3, slowk_matype=0,
                    slowd_period=3, slowd_matype=0)[0][-1]


def sto_slow_d(stockData, point):
    return \
        talib.STOCH(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], fastk_period=5,
                    slowk_period=3, slowk_matype=0,
                    slowd_period=3, slowd_matype=0)[1][-1]


# STOCHF - Stochastic Fast
def sto_fast_k(stockData, point):
    return \
        talib.STOCHF(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], fastk_period=5,
                     fastd_period=3, fastd_matype=0)[0][-1]


def sto_fast_d(stockData, point):
    return \
        talib.STOCHF(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], fastk_period=5,
                     fastd_period=3, fastd_matype=0)[1][-1]


# STOCHRSI - Stochastic Relative Strength Index
def sto_rsi_fast_d(stockData, point, period):
    return \
        talib.STOCHRSI(stockData['close'][:point], timeperiod=period, fastk_period=5, fastd_period=3, fastd_matype=0)[0][-1]


def sto_rsi_fast_d(stockData, point, period):
    return \
        talib.STOCHRSI(stockData['close'][:point], timeperiod=period, fastk_period=5, fastd_period=3, fastd_matype=0)[1][-1]


# TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
def trix(stockData, point):
    return talib.TRIX(stockData['close'][:point], timeperiod=30)[-1]


# ULTOSC - Ultimate Oscillator
def ult_osc(stockData, point):
    return talib.ULTOSC(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], timeperiod1=7,
                        timeperiod2=14,
                        timeperiod3=28)[-1]


# WILLR - Williams' %R
def williams(stockData, point):
    return talib.WILLR(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], timeperiod=14)[-1]


''' _________________ Volume Indicators _________________ '''


# AD - Chaikin A/D Line
def ad_chaikin(stockData, point):
    volume = np.array(stockData['volume'][:point], dtype='d')
    return talib.AD(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], volume)[-1]


# ADOSC - Chaikin A/D Oscillator
def adosc_chaikin(stockData, point):
    volume = np.array(stockData['volume'][:point], dtype='d')
    return talib.ADOSC(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], volume,
                       fastperiod=3, slowperiod=10)[-1]


# OBV - On Balance Volume
def obv(stockData, point):
    volume = np.array(stockData['volume'][:point], dtype='d')
    return talib.OBV(stockData['close'][:point], volume)[-1]


''' _________________ Volatility Indicators _________________ '''


# ATR - Average True Range
def atr(stockData, point):
    return talib.ATR(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], timeperiod=14)[-1]


# NATR - Normalized Average True Range
def natr(stockData, point):
    return talib.NATR(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point], timeperiod=14)[-1]


# TRANGE - True Range
def true_range(stockData, point):
    return talib.TRANGE(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point])[-1]


''' _________________ Price Transform _________________'''


# AVGPRICE - Average Price
def average_price(stockData, point):
    return talib.AVGPRICE(stockData['open'][:point], stockData['high'][:point], stockData['low'][:point], stockData['close'][:point])[-1]


# MEDPRICE - Median Price
def median_price(stockData, point):
    return talib.MEDPRICE(stockData['high'][:point], stockData['low'][:point])[-1]


# TYPPRICE - Typical Price
def typical_price(stockData, point):
    return talib.TYPPRICE(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point])[-1]


# WCLPRICE - Weighted Close Price
def weighted_close_price(stockData, point):
    return talib.WCLPRICE(stockData['high'][:point], stockData['low'][:point], stockData['close'][:point])[-1]


