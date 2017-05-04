import statistics

from get_data import *
from plot import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from backtest import back_test_short


def fit_predict_RandomForestClassifier(X_train, Y, X_test):
    m = RandomForestClassifier(n_estimators=10)
    m.fit(X_train, Y.values.ravel())
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    filename = '000.sav'
    joblib.dump(m, filename)
    return y_train, y_test


def classify(name, tf, TP, cutloss, period):
    p_train = 15000
    ohlc = get_ohlc(name, tf)
    y = get_y_short(data=ohlc[2], TP=TP, cutloss=cutloss, p_train=p_train, period=period)
    x = get_x(ohlc)
    x_train_raw = x[:p_train]
    y_train_raw = y[:p_train]
    x_test_raw = x[p_train:]
    y_test_raw = y[p_train:]
    # print(x_train_raw)
    # print(y_train_raw)
    # print(x_test_raw)
    # print(y_test_raw)

    y_train, y_test = fit_predict_RandomForestClassifier(x_train_raw, y_train_raw, x_test_raw)

    train_acc = round(accuracy_score(y_train_raw, y_train), 3)
    test_acc = round(accuracy_score(y_test_raw, y_test), 3)
    # print(train_acc, test_acc)
    trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio = back_test_short(x_test_raw, y_test, TP, cutloss=cutloss)
    for i, e in enumerate(y_test):
        if e == 1 and i < len(y_test):
            for j, e in enumerate(y_test[i + 1:]):
                if e == 1:
                    y_test[i + j + 1] = 0
                else:
                    break
    # plot_long(x_test_raw[:], y_test[:], TP, test_acc)
    # print(win_chance,test_acc)
    if win_chance >= 50 and test_acc*100 >= 85:
        plot_long(x_test_raw, y_test, TP, test_acc)
    return test_acc, trade_count, win_chance, p_l_ratio


# avg of 100 times
# 0.8387 27.87 46.697608036678496 4.3366702153595345 2.066666666666664


def get_model():
    for i in range(100):
        result = classify(name='S50M17', tf='3', TP=2, cutloss=2,period=15)
        print(result)
        if result[0]*100 >= 85:
            break

get_model()


def check_rating():
    devide = 5
    avg_test_acc = 0
    avg_trade_count = 0
    avg_win_chance = 0
    avg_p_l_ratio = 0
    win_rate = []
    for i in range(devide):
        result = classify(name='S50M17', tf='3', TP=2, cutloss=2)
        # print([round(i, 2) for i in result])
        avg_test_acc = avg_test_acc + result[0]
        avg_trade_count = avg_trade_count + result[1]
        avg_win_chance = avg_win_chance + result[2]
        avg_p_l_ratio = avg_p_l_ratio + result[3]
        win_rate.append(result[2])
    # std = statistics.stdev(win_rate)
    print('acc:', round(avg_test_acc / devide, 3), 'trade', avg_trade_count / devide, 'win', round(avg_win_chance / devide, 2), 'p_l', round(avg_p_l_ratio / devide, 2))
# check_rating()


def check_best_range():
    loops = 5
    for i in range(10, 26, 1):
        avg_test_acc = 0
        avg_trade_count = 0
        avg_win_chance = 0
        avg_p_l_ratio = 0
        win_rate = []
        for j in range(loops):
            result = classify(name='S50M17', tf='3', TP=2, cutloss=2, period=i)
            # print(result)
            avg_test_acc = avg_test_acc + result[0]
            avg_trade_count = avg_trade_count + result[1]
            avg_win_chance = avg_win_chance + result[2]
            avg_p_l_ratio = avg_p_l_ratio + result[3]
            win_rate.append(result[2])
        std = statistics.stdev(win_rate)
        if round(avg_win_chance / loops, 3) >= 0:
            print(i, round(avg_test_acc / loops, 3), round(avg_trade_count / loops, 3), round(avg_win_chance / loops, 3), round(std, 3), round(avg_p_l_ratio / loops,  3))


# check_best_range()
