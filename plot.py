import logging
import os
import re

from bokeh.plotting import figure, output_file, show
from sklearn.externals import joblib

logging.getLogger("requests").setLevel(logging.WARNING)


def plot_long(x, y, TP, test_acc):
    plt_cls = x['CLOSE'].tolist()
    is_up = []
    value = []
    for i, item in enumerate(y.tolist()):
        if item == 1:
            is_up.append(i)
            value.append(plt_cls[i])
    f_name = str(TP) + '_' + str(round(test_acc, 2))
    os.remove('predict_plot.html')
    output_file("predict_plot.html", title=f_name)
    p = figure(plot_width=1500, plot_height=800, x_axis_label=f_name)
    p.line([i for i in range(int(len(plt_cls)))], plt_cls, line_width=1.5, color='grey')
    p.circle(is_up, value, color="orange", size=5)
    # p.circle(is_up, [i - 1.5 for i in value], fill_color="red", size=5)
    # p.circle(is_up, [i + TP for i in value], fill_color="green", size=5)
    show(p)


def plot_pl(close, trade_index, bt):
    colors = []
    index = []
    b_value = []

    for i, item in enumerate(trade_index):
        b_value.append(close[item[0]])
        index.append(item[0])
        colors.append(item[1])
    os.remove('bd.html')
    output_file("bd.html", title='plot after backtest')
    p = figure(plot_width=1500, plot_height=800, x_axis_label='plot after backtest')
    p.line([i for i in range(int(len(close)))], close, line_width=1.5, color='grey')
    p.circle(index, b_value, color=colors, size=5)
    show(p)


def plot_full_predict():
    from get_data import get_ohlc, get_x
    ohlc = get_ohlc('S50U17', '3')
    # y = get_y_long(data=ohlc[2], TP=3.2, cutloss=0.8)
    x = get_x(ohlc)
    range_of_p = 0
    X = x[range_of_p:]
    fname = 'L_T3.2_C0.8_W42_R3.3.sav'
    predict = joblib.load(fname).predict(X)
    predict = predict.tolist()
    print(predict, '\n', len(predict))
    split_fname = re.split('_', fname)
    TP = float(split_fname[1][1:])
    print(TP)
    cutloss = 1.5
    print(TP, cutloss)
    close = X['CLOSE'].tolist()
    trade_count = 0
    profit_count = 0
    loss_count = 0
    trade_index = []
    HOLD = False
    BUY_PRICE = 0
    for i, item in enumerate(close):
        if HOLD is True:
            diff = item - BUY_PRICE
            if diff >= TP:
                profit_count = profit_count + 1
                trade_index.append((i, 'green'))
                HOLD = False
            if diff <= -cutloss:
                loss_count = loss_count + 1
                trade_index.append((i, 'red'))
                HOLD = False
        else:
            if predict[i] == 1:
                HOLD = True
                BUY_PRICE = item
                trade_count = trade_count + 1
                trade_index.append((i, 'blue'))
    cutloss = cutloss * 1
    profit_sum = profit_count * TP
    loss_sum = loss_count * cutloss

    colors = []
    index = []
    b_value = []

    for i, item in enumerate(trade_index):
        b_value.append(close[item[0]])
        index.append(item[0])
        colors.append(item[1])
    output_file("prediction.html", title='prediction')
    p = figure(plot_width=1500, plot_height=800, x_axis_label='prediction')
    p.line([i for i in range(int(len(close)))], close, line_width=1.5, color='grey')
    p.circle(index, b_value, color=colors, size=5)
    show(p)
plot_full_predict()