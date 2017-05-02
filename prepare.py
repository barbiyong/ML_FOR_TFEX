import logging
logging.getLogger("requests").setLevel(logging.WARNING)

from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from bokeh.plotting import figure, output_file, show
import pandas as pd

from talib_wrapper import get_ema, get_macd, get_rsi_7
from get_data import get_ohlc
from plot import plot_long
from backtest import back_test


def get_y_long(data, period, delim):
    slice = 500
    cutloss = -1.5
    data = [float(i) for i in data]
    ret_list = []
    count = 0
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
    count = 0
    for i in ret_list:
        if i == 1:
            count = count + 1
    # print(count, len(ret_list), count / len(ret_list))

    output_file("raw.html", title='raw data')
    for item in ret_list:
        if item == 1:
            count = count + 1
    # print(count / len(ret_list))

    p_data = data[slice + 10000:]
    is_up = []
    value = []

    for i, item in enumerate(ret_list[slice + 10000:]):
        if item == 1:
            is_up.append(i)
            value.append(p_data[i])

    p = figure(plot_width=1500, plot_height=800, x_axis_label='raw')
    p.line([i for i in range(int(len(p_data)))], p_data, line_width=1.5, color='grey')
    p.circle(is_up, value, fill_color="green", size=5)
    # p.circle(is_up, [i - 1.5 for i in value], fill_color="red", size=8)
    # p.circle(is_up, [i + delim for i in value], fill_color="green", size=8)
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
    MACD, SIGNAL, HIST = get_macd(closes=ohlc[2])

    df = pd.DataFrame(
        {'OPEN': ohlc[1][slice:], 'CLOSE': ohlc[2][slice:], 'HIGH': ohlc[3][slice:], 'LOW': ohlc[4][slice:], 'EMA5': EMA5[slice:], 'EMA10': EMA10[slice:], 'EMA25': EMA25[slice:],
         'EMA50': EMA50[slice:], 'EMA75': EMA75[slice:], 'EMA200': EMA200[slice:], 'RSI7': RSI7[slice:], 'MACD': MACD[slice:], 'SIGNAL': SIGNAL[slice:], 'HIST': HIST[slice:]})

    return df


def fit_predict_RandomForestClassifier(X_train, Y, X_test):
    m = RandomForestClassifier(n_estimators=10)
    m.fit(X_train, Y.values.ravel())
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    filename = 'L_00_0_0_v0.sav'
    # os.remove('L_20_3.1_00_v0.sav')
    joblib.dump(m, filename)
    return y_train, y_test


def classify(name, tf, period, delim):
    ohlc = get_ohlc(name, tf)
    y = get_y_long(data=ohlc[2], period=period, delim=delim)
    x = get_x(ohlc)

    x_train_raw = x[:10000]
    y_train_raw = y[:10000]
    x_test_raw = x[10000:]
    y_test_raw = y[10000:]
    # print(x_train_raw)
    # print(y_train_raw)
    # print(x_test_raw)
    # print(y_test_raw)

    y_train, y_test = fit_predict_RandomForestClassifier(x_train_raw, y_train_raw, x_test_raw)

    train_acc = round(accuracy_score(y_train_raw, y_train), 3)
    test_acc = round(accuracy_score(y_test_raw, y_test), 3)
    # print(train_acc, test_acc)
    trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio = back_test(data=x_test_raw, predict=y_test, delim=delim)
    if win_chance >= 55:
        plot_long(x_test_raw, y_test, period, delim, test_acc)
    return test_acc, trade_count, win_chance, p_l_ratio


def main():
    result = classify('S50M17', '3', 20, 3.5)

    # avg_test_acc = 0
    # avg_trade_count = 0
    # avg_win_chance = 0
    # avg_p_l_ratio = 0
    #
    # for i in range(100):
    #     print(i)
    #     result = classify('S50M17', '3', 40, 3.5)
    #     avg_test_acc = avg_test_acc + result[0]
    #     avg_trade_count = avg_trade_count + result[1]
    #     avg_win_chance = avg_win_chance + result[2]
    #     avg_p_l_ratio = avg_p_l_ratio + result[3]
    #
    # print(avg_test_acc/100, avg_trade_count/100, avg_win_chance/100, avg_p_l_ratio/100)


main()
