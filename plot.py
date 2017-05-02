from bokeh.plotting import figure, output_file, show
import logging
import os
logging.getLogger("requests").setLevel(logging.WARNING)


def plot_long(x, y, period, delim, test_acc):
    plt_cls = x['CLOSE'].tolist()
    is_up = []
    value = []
    for i, item in enumerate(y.tolist()):
        if item == 1:
            is_up.append(i)
            value.append(plt_cls[i])
    f_name = str(period) + '_' + str(delim) + '_' + str(round(test_acc, 2))
    os.remove('predict_plot.html')
    output_file("predict_plot.html", title=f_name)
    p = figure(plot_width=1500, plot_height=800, x_axis_label=f_name)
    p.line([i for i in range(int(len(plt_cls)))], plt_cls, line_width=1.5, color='grey')
    p.circle(is_up, value, color="orange", size=5)
    # p.circle(is_up, [i - 1.5 for i in value], fill_color="red", size=5)
    # p.circle(is_up, [i + delim for i in value], fill_color="green", size=5)
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
