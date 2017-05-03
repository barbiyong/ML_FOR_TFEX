from sklearn.externals import joblib
from get_data import get_ohlc, get_x
from datetime import datetime
import sched, time

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
    print(predict_a[-1], predict_b[-1], predict_c[-1])
    if have is True:
        if b_price - close[-1] >= 0.8:
            is_buy = 'CUT LOSS NOW'
        elif predict_a[-1] == 1:
            is_buy = 'A: WAIT TO SELL MORE AT -  ' + str(round(close[-1] + 3.2, 1))
        elif predict_b[-1] == 1:
            is_buy = 'B: WAIT TO SELL MORE AT -  ' + str(round(close[-1] + 3.2, 1))
        else:
            is_buy = 'A/B: NONE'
        if predict_c[-1] == 1:
            is_sell = 'C: WARNING TO SELL'
        else:
            is_sell = 'C: NONE'

    if have is False:
        if predict_a[-1] == 1:
            is_buy = 'A: BUY TO SELL AT -  ' + str(round(close[-1] + 3.2, 1))
        elif predict_b[-1] == 1:
            is_buy = 'B: BUY TO SELL AT -  ' + str(round(close[-1] + 3.2, 1))
        else:
            is_buy = 'A/B: NONE'
        if predict_c[-1] == 1:
            is_sell = 'C: WAIT TO BUY'
        else:
            is_sell = 'C: NONE'

    ret_string = str(close[-1]) + ' @ ' + str(date[-1]) + '   ---|>   ' + str(is_buy) + '   |||   ' + str(is_sell)
    return ret_string


def main():
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    fname_a = 'L_T3.2_C0.8_W53_R4.0.sav'
    fname_b = 'L_T3.2_C0.8_W42_R3.3.sav'
    fname_c = 'S_T2.0_C1.3_W42_R1.8.sav'
    ohlc = get_ohlc('S50M17', '3')
    ohlc = [i[:] for i in ohlc]
    predict_a = joblib.load(fname_a).predict(get_x(ohlc))
    predict_b = joblib.load(fname_b).predict(get_x(ohlc))
    predict_c = joblib.load(fname_c).predict(get_x(ohlc))
    predict_a = predict_a.tolist()
    predict_b = predict_b.tolist()
    predict_c = predict_c.tolist()
    predict_len_a = len(predict_a)
    predict_len_b = len(predict_b)
    predict_len_c = len(predict_c)
    predict_len = predict_len_a if predict_len_a == predict_len_b else 0
    date = ohlc[0][len(ohlc[0]) - predict_len:]
    close = ohlc[1][len(ohlc[1]) - predict_len:]
    if len(date) == len(close):
        print("Get result...")
        print('-----', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '-----')
        print('A: L_T3.2_C0.8_W53_R4.0', '  B: L_T3.2_C0.8_W42_R3.3', '  C: S_T2.0_C1.3_W42_R1.8')
        print('\nNOW')
        print(now_state(date, close, predict_a, predict_b, predict_c, False, 0))
        # print('\nNOW [HAVE POSITION]')
        # print(now_state(date, close, predict_a, predict_b, predict_c, True, 985))
        print('\nLAST PREDICT')
        print(last_predict(date, close, predict_a, predict_b, predict_c))
    s.enter(60, 1, main, ())

if __name__ == '__main__':
    s = sched.scheduler(time.time, time.sleep)
    s.enter(60, 1, main, ())
    s.run()
