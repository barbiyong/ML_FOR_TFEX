from plot import plot_pl
import logging
logging.getLogger("requests").setLevel(logging.WARNING)


def back_test(data, predict, delim):
    trade_count = 0
    profit_count = 0
    loss_count = 0
    close = data['CLOSE'].tolist()
    trade_index = []
    HOLD = False
    for i, item in enumerate(close):
        if HOLD is True:
            for j, next_item in enumerate(close[i:]):
                diff = next_item - item
                if diff >= delim:
                    profit_count = profit_count + 1
                    trade_count = trade_count + 1
                    trade_index.append((i, 'green'))
                    HOLD = False
                    break
                if diff <= -2:
                    loss_count = loss_count + 1
                    trade_count = trade_count + 1
                    trade_index.append((i, 'red'))
                    HOLD = False
                    break
        else:
            if predict[i] == 1:
                HOLD = True

    profit_sum = profit_count * delim
    loss_sum = profit_count * 1.5
    try:
        win_chance = (profit_count / trade_count)*100
        p_l_ratio = profit_sum / loss_sum
    except:
        win_chance = 0
        p_l_ratio = 0
    # if win_chance >= 55:
    #     plot_pl(close, trade_index, [trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio])
    # print('trade_count:', trade_count, 'profit_count:', profit_count, 'loss_count:', loss_count, 'profit_sum:', profit_sum, 'loss_sum:', loss_sum, 'win_chance:', win_chance, 'p_l_ratio:', p_l_ratio)
    return trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio
