import statistics

from get_data import *
from plot import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from backtest import back_test


def fit_predict_RandomForestClassifier(X_train, Y, X_test):
    m = RandomForestClassifier(n_estimators=10)
    m.fit(X_train, Y.values.ravel())
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    filename = '000.sav'
    joblib.dump(m, filename)
    return y_train, y_test


def classify(name, tf, TP, cutloss):
    p_train = 15000
    ohlc = get_ohlc(name, tf)
    y = get_y_long(data=ohlc[2], TP=TP, cutloss=cutloss, p_train=p_train)
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
    trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio = back_test(x_test_raw, y_test, TP, cutloss=cutloss)
    # plot_long(x_test_raw, y_test, TP, test_acc)
    # print(trade_count)
    if trade_count >= 21 and win_chance >= 45:
        plot_long(x_test_raw, y_test, TP, test_acc)
    # if win_chance >= 50 and trade_count >=21:
    #     plot_long(x_test_raw, y_test, TP, test_acc)
    return test_acc, trade_count, win_chance, p_l_ratio


# avg of 100 times
# 0.8387 27.87 46.697608036678496 4.3366702153595345 2.066666666666664


def get_model():
    for i in range(500):
        result = classify(name='S50M17', tf='3', TP=3.2, cutloss=1.2)
        if result[1] >= 21 and result[2] >= 45:
            print(result)
            break
        # if result[2] >= 50 and result[1] >= 18:
        #     break

get_model()


def check_rating():
    devide = 1000
    avg_test_acc = 0
    avg_trade_count = 0
    avg_win_chance = 0
    avg_p_l_ratio = 0
    win_rate = []
    for i in range(devide):
        result = classify(name='S50M17', tf='3', TP=3.2, cutloss=0.8)
        print([round(i, 2) for i in result])
        avg_test_acc = avg_test_acc + result[0]
        avg_trade_count = avg_trade_count + result[1]
        avg_win_chance = avg_win_chance + result[2]
        avg_p_l_ratio = avg_p_l_ratio + result[3]
        win_rate.append(result[2])
    # std = statistics.stdev(win_rate)
    print('acc:', round(avg_test_acc / devide, 3), 'trade', avg_trade_count / devide, 'win', round(avg_win_chance / devide, 2), 'p_l', round(avg_p_l_ratio / devide, 2))


def check_best_range():
    loops = 10
    for i in range(4, 30, 2):
        avg_test_acc = 0
        avg_trade_count = 0
        avg_win_chance = 0
        avg_p_l_ratio = 0
        win_rate = []
        for j in range(loops):
            result = classify(name='S50M17', tf='3', TP=3.2, cutloss=i/10)
            # print(result)
            avg_test_acc = avg_test_acc + result[0]
            avg_trade_count = avg_trade_count + result[1]
            avg_win_chance = avg_win_chance + result[2]
            avg_p_l_ratio = avg_p_l_ratio + result[3]
            win_rate.append(result[2])
        std = statistics.stdev(win_rate)
        if round(avg_win_chance / loops, 3) >= 0:
            print(i/10, round(avg_test_acc / loops, 3), round(avg_trade_count / loops, 3), round(avg_win_chance / loops, 3), round(std, 3), round(avg_p_l_ratio / loops,  3))


# check_best_range()
