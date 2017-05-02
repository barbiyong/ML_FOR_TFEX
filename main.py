import logging
logging.getLogger("requests").setLevel(logging.WARNING)

from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from bokeh.plotting import figure, output_file, show
import pandas as pd
import statistics
import os

from talib_wrapper import *
from get_data import get_ohlc
from plot import plot_long
from backtest import back_test


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

    # train plott
    # os.remove('train_data.html')
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
    # show(p)
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


def fit_predict_RandomForestClassifier(X_train, Y, X_test):
    m = RandomForestClassifier(n_estimators=10)
    m.fit(X_train, Y.values.ravel())
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    filename = 'L_TF3_35_3.1_V1.sav'
    joblib.dump(m, filename)
    return y_train, y_test


def classify(name, tf, period, delim, cutloss):
    ohlc = get_ohlc(name, tf)
    y = get_y_long(data=ohlc[2], period=period, delim=delim, cutloss=cutloss)
    x = get_x(ohlc)

    x_train_raw = x[:10000]
    y_train_raw = y[:10000]
    x_test_raw = x[14000:]
    y_test_raw = y[14000:]
    # print(x_train_raw)
    # print(y_train_raw)
    # print(x_test_raw)
    # print(y_test_raw)

    y_train, y_test = fit_predict_RandomForestClassifier(x_train_raw, y_train_raw, x_test_raw)

    train_acc = round(accuracy_score(y_train_raw, y_train), 3)
    test_acc = round(accuracy_score(y_test_raw, y_test), 3)
    # print(train_acc, test_acc)
    trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio = back_test(data=x_test_raw, predict=y_test, delim=delim, cutloss=cutloss)
    # if win_chance >= 50:
    #     plot_long(x_test_raw, y_test, period, delim, test_acc)
    return test_acc, trade_count, win_chance, p_l_ratio

# avg of 100 times
# 0.8387 27.87 46.697608036678496 4.3366702153595345 2.066666666666664


def main():
    # avg_test_acc = 0
    # avg_trade_count = 0
    # avg_win_chance = 0
    # avg_p_l_ratio = 0
    # win_rate = []
    # for i in range(100):
    #     result = classify(name='S50M17', tf='3', period=35, delim=3.1, cutloss=1.5)
    #     avg_test_acc = avg_test_acc + result[0]
    #     avg_trade_count = avg_trade_count + result[1]
    #     avg_win_chance = avg_win_chance + result[2]
    #     avg_p_l_ratio = avg_p_l_ratio + result[3]
    #     win_rate.append(result[2])
    # std = statistics.stdev(win_rate)
    # print(i, avg_test_acc / 100, avg_trade_count / 100, avg_win_chance / 100, std, avg_p_l_ratio / 100)

    for i in range(1000):
        result = classify(name='S50M17', tf='3', period=35, delim=3.1, cutloss=1.5)
        if result[1] >= 5:
            break

    # for i in range(30, 50, 5):
    #     avg_test_acc = 0
    #     avg_trade_count = 0
    #     avg_win_chance = 0
    #     avg_p_l_ratio = 0
    #     for k in range(100):
    #         result = classify('S50M17', '3', i, 3.1, 1.5)
    #         avg_test_acc = avg_test_acc + result[0]
    #         avg_trade_count = avg_trade_count + result[1]
    #         avg_win_chance = avg_win_chance + result[2]
    #         avg_p_l_ratio = avg_p_l_ratio + result[3]
    #     if avg_win_chance/100 > 0:
    #         print(i, avg_test_acc/100, avg_trade_count/100, avg_win_chance/100, avg_p_l_ratio/100)

    # for i in range(50):
        # result = classify('S50M17', '3', 20, 5)

main()
