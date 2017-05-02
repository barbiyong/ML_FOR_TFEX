import math
import talib
import numpy as np
from decimal import Decimal


def get_ema(closes, period: int):
    closes = np.array(closes, dtype=float)
    ema = talib.EMA(closes, timeperiod=period)
    return ema


def get_rsi_7(closes):
    closes = np.array(closes, dtype=float)
    rsi = talib.RSI(closes, timeperiod=7)
    return rsi


def get_macd(closes):
    closes = np.array(closes, dtype=float)
    macd, macdsignal, macdhist = talib.MACD(closes, 12, 26, 9)
    return macd, macdsignal, macdhist


def get_bbands(closes):
    closes = np.array(closes, dtype=float)
    upper, middle, lower = talib.BBANDS(closes)
    return upper, middle, lower


def get_adx(high, low, closes):
    high = np.array(high, dtype=float)
    low = np.array(low, dtype=float)
    closes = np.array(closes, dtype=float)
    rsi = talib.ADX(high, low, closes, timeperiod=14)
    return rsi


def get_pdi(high, low, closes):
    high = np.array(high, dtype=float)
    low = np.array(low, dtype=float)
    closes = np.array(closes, dtype=float)
    rsi = talib.MINUS_DI(high, low, closes, timeperiod=14)
    return rsi


def get_ndi(high, low, closes):
    high = np.array(high, dtype=float)
    low = np.array(low, dtype=float)
    closes = np.array(closes, dtype=float)
    rsi = talib.MINUS_DI(high, low, closes, timeperiod=14)
    return rsi