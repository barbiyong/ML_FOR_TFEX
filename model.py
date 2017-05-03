from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import statistics
from plot import *
from backtest import back_test
from get_data import *


def fit_predict_RandomForestClassifier(X_train, Y, X_test):
    m = RandomForestClassifier(n_estimators=10)
    m.fit(X_train, Y.values.ravel())
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    filename = '000.sav'
    joblib.dump(m, filename)
    return y_train, y_test


def classify(name, tf, period, delim, cutloss):
    ohlc = get_ohlc(name, tf)
    y = get_y_long(data=ohlc[2], period=period, delim=delim, cutloss=cutloss)
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
    trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio = back_test(data=x_test_raw, predict=y_test, delim=delim, cutloss=cutloss)
    # if win_chance >= 50:
    #     plot_long(x_test_raw, y_test, period, delim, test_acc)
    return test_acc, trade_count, win_chance, p_l_ratio

# avg of 100 times
# 0.8387 27.87 46.697608036678496 4.3366702153595345 2.066666666666664


def get_model():

    avg_test_acc = 0
    avg_trade_count = 0
    avg_win_chance = 0
    avg_p_l_ratio = 0
    win_rate = []
    for i in range(10):
        result = classify(name='S50M17', tf='3', period=35, delim=3.1, cutloss=1.5)
        print(result)
        avg_test_acc = avg_test_acc + result[0]
        avg_trade_count = avg_trade_count + result[1]
        avg_win_chance = avg_win_chance + result[2]
        avg_p_l_ratio = avg_p_l_ratio + result[3]
        win_rate.append(result[2])
    std = statistics.stdev(win_rate)
    print('acc:', round(avg_test_acc / 10), 'trade', avg_trade_count / 10, 'win', round(avg_win_chance / 10, 2), 'p_l', round(avg_p_l_ratio / 10, 2))

    # for i in range(1000):
    #     result = classify(name='S50M17', tf='3', period=35, delim=3.1, cutloss=1.5)
    #     if result[1] >= 5:
    #         break

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

# get_model()


def check_best_range():
    for i in range(5, 100, 5):
        avg_test_acc = 0
        avg_trade_count = 0
        avg_win_chance = 0
        avg_p_l_ratio = 0
        win_rate = []
        for j in range(100):
            result = classify(name='S50M17', tf='3', period=i, delim=2.2, cutloss=0.8)
            # print(result)
            avg_test_acc = avg_test_acc + result[0]
            avg_trade_count = avg_trade_count + result[1]
            avg_win_chance = avg_win_chance + result[2]
            avg_p_l_ratio = avg_p_l_ratio + result[3]
            win_rate.append(result[2])
        std = statistics.stdev(win_rate)
        if avg_win_chance / 100 >= 50:
            print(i, avg_test_acc / 100, avg_trade_count / 100, avg_win_chance / 100, std, avg_p_l_ratio / 100)
check_best_range()


def check_best_TP():
    for i in range(20, 52, 2):
        avg_test_acc = 0
        avg_trade_count = 0
        avg_win_chance = 0
        avg_p_l_ratio = 0
        win_rate = []
        for j in range(10):
            result = classify(name='S50M17', tf='3', period=25, delim=i/10, cutloss=0.8)
            avg_test_acc = avg_test_acc + result[0]
            avg_trade_count = avg_trade_count + result[1]
            avg_win_chance = avg_win_chance + result[2]
            avg_p_l_ratio = avg_p_l_ratio + result[3]
            win_rate.append(result[2])
        std = statistics.stdev(win_rate)
        print(i, avg_test_acc / 10, avg_trade_count / 10, avg_win_chance / 10, std, avg_p_l_ratio / 10)
# check_best_TP()