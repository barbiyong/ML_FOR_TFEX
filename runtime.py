from sklearn.externals import joblib
from get_data import get_ohlc, get_x
from datetime import datetime
from plot import plot_run_time
import threading


def last_predict(date, close, predict_a, predict_b, predict_c):
    last_buy_predict_a = 0
    last_buy_predict_b = 0
    last_buy_predict_c = 0
    for i, e in enumerate(predict_a):
        if predict_a[i] == 1:
            last_buy_predict_a = i
        if predict_b[i] == 1:
            last_buy_predict_b = i
        if predict_c[i] == 1:
            last_buy_predict_c = i

    ret_string = 'A ' + str(close[last_buy_predict_a]) + ' @ ' + str(date[last_buy_predict_a] + '  DIFF = ' + str(round(close[-1] - close[last_buy_predict_a], 1)))
    ret_string = ret_string + '\nB ' + str(close[last_buy_predict_b]) + ' @ ' + str(date[last_buy_predict_b] + '  DIFF = ' + str(round(close[-1] - close[last_buy_predict_b], 1)))
    ret_string = ret_string + '\nC ' + str(close[last_buy_predict_c]) + ' @ ' + str(date[last_buy_predict_c] + '  DIFF = ' + str(round(close[-1] - close[last_buy_predict_c], 1)))
    print(last_buy_predict_a, last_buy_predict_b, last_buy_predict_c)
    return ret_string


def now_state(date, close, predict_a, predict_b, predict_c, have, b_price):
    alert = False
    print(predict_a[-1], predict_b[-1], predict_c[-1])
    # for i, e in enumerate(predict_c):
    #     if e == 1:
    #         print(date[i])
    if have is True:
        if b_price - close[-1] >= 0.8:
            is_buy = 'CUT LOSS NOW'
            alert = True
        elif predict_a[-1] == 1:
            is_buy = 'A: WAIT TO SELL MORE AT -  ' + str(round(close[-1] + 3.2, 1))
            alert = True
        elif predict_b[-1] == 1:
            is_buy = 'B: WAIT TO SELL MORE AT -  ' + str(round(close[-1] + 3.2, 1))
            alert = True
        else:
            is_buy = 'A/B: NONE'
        if predict_c[-1] == 1:
            is_sell = 'C: WARNING TO SELL'
            alert = True
        else:
            is_sell = 'C: NONE'

    if have is False:
        if predict_a[-1] == 1:
            is_buy = 'A: BUY TO SELL AT -  ' + str(round(close[-1] + 3.2, 1))
            alert = True
        elif predict_b[-1] == 1:
            is_buy = 'B: BUY TO SELL AT -  ' + str(round(close[-1] + 3.2, 1))
            alert = True
        else:
            is_buy = 'A/B: NONE'
        if predict_c[-1] == 1:
            is_sell = 'C: WARNING'
            alert = True
        else:
            is_sell = 'C: NONE'
    ret_string = str(close[-1]) + ' @ ' + str(date[-1]) + '   ---|>   ' + str(is_buy) + '   |||   ' + str(is_sell)
    return ret_string, alert


def reduce(pa, pb, pc):
    for i, e in enumerate(pc):
        if e == 1 and i < len(pc):
            for j, e in enumerate(pc[i + 1:]):
                if e == 1:
                    pc[i + j + 1] = 0
                else:
                    break
    for i, e in enumerate(pa):
        if e == 1 and i < len(pa):
            for j, e in enumerate(pa[i + 1:]):
                if e == 1:
                    pa[i + j + 1] = 0
                else:
                    break

    for i, e in enumerate(pb):
        if e == 1 and i < len(pb):
            for j, e in enumerate(pb[i + 1:]):
                if e == 1:
                    pb[i + j + 1] = 0
                else:
                    break
    return pa, pb, pc


def main():
    threading.Timer(180.0, main).start()  # called every 3 minute
    fname_a = 'L_T3.2_C1.2_W46_R2.4.sav'
    fname_b = 'L_T3.2_C1.2_W53_R3.0.sav'
    fname_c = 'S_T2.0_C2.0_W53_R1.3.sav'
    ohlc = get_ohlc('S50M17', '3')
    ohlc = [i[:] for i in ohlc]
    predict_a = joblib.load(fname_a).predict(get_x(ohlc))
    predict_b = joblib.load(fname_b).predict(get_x(ohlc))
    predict_c = joblib.load(fname_c).predict(get_x(ohlc))
    predict_a = predict_a.tolist()
    predict_b = predict_b.tolist()
    predict_c = predict_c.tolist()
    predict_a, predict_b, predict_c = reduce(predict_a, predict_b, predict_c)
    predict_len_a = len(predict_a)
    predict_len_b = len(predict_b)
    predict_len_c = len(predict_c)
    predict_len = predict_len_a if predict_len_a == predict_len_b else 0
    date = ohlc[0][len(ohlc[0]) - predict_len:]
    close = ohlc[1][len(ohlc[1]) - predict_len:]
    if len(date) == len(close):
        ret_string, alert = now_state(date, close, predict_a, predict_b, predict_c, False, 0)
        print("\n\n\nGet result...")
        print('-----', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '-----')
        if alert is True:
            print('A: L_T3.2_C1.2_W46_R2.4', '  B: L_T3.2_C1.2_W53_R3.0', '  C: S_T2.0_C2.0_W53_R1.3')
            print('\nNOW')
            print('\n********************************')
            print('**********************************')
            print('**********************************\n')
            print(ret_string)
            print('\n********************************')
            print('**********************************')
            print('**********************************')
            print('\nLAST PREDICT')
            print(last_predict(date, close, predict_a, predict_b, predict_c))
        else:
            print('\nNONE')
        pl = -500
        plot_run_time(date[pl:], close[pl:], predict_a[pl:], predict_b[pl:], predict_c[pl:])


if __name__ == '__main__':
    main()
