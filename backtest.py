from plot import plot_pl


def back_test(data, predict, TP, cutloss):
    trade_count = 0
    profit_count = 0
    loss_count = 0
    close = data['CLOSE'].tolist()
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
    try:
        win_chance = (profit_count / trade_count)*100
        p_l_ratio = profit_sum / loss_sum
    except:
        win_chance = 0
        p_l_ratio = 0

    # plot_pl(close, trade_index, [trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio])
    if win_chance >= 40 and trade_count >= 19:
        plot_pl(close, trade_index, [trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio])
        print('trade_count:', trade_count, 'profit_count:', profit_count, 'loss_count:', loss_count, 'profit_sum:', profit_sum, 'loss_sum:', loss_sum, 'win_chance:', win_chance,
              'p_l_ratio:', p_l_ratio)
    # print('trade_count:', trade_count, 'profit_count:', profit_count, 'loss_count:', loss_count, 'profit_sum:', profit_sum, 'loss_sum:', loss_sum, 'win_chance:', win_chance, 'p_l_ratio:', p_l_ratio)
    return trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio



def back_test_short(data, predict, TP, cutloss):
    trade_count = 0
    profit_count = 0
    loss_count = 0
    close = data['CLOSE'].tolist()
    trade_index = []
    HOLD = False
    BUY_PRICE = 0
    for i, item in enumerate(close):
        if HOLD is True:
            diff = item - BUY_PRICE
            if diff <= TP*-1:
                profit_count = profit_count + 1
                trade_index.append((i, 'green'))
                HOLD = False
            if diff >= cutloss:
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
    try:
        win_chance = (profit_count / trade_count)*100
        p_l_ratio = profit_sum / loss_sum
    except:
        win_chance = 0
        p_l_ratio = 0

    plot_pl(close, trade_index, [trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio])
    # if win_chance >= 40 and trade_count >= 19:
    #     plot_pl(close, trade_index, [trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio])
    #     print('trade_count:', trade_count, 'profit_count:', profit_count, 'loss_count:', loss_count, 'profit_sum:', profit_sum, 'loss_sum:', loss_sum, 'win_chance:', win_chance,
    #           'p_l_ratio:', p_l_ratio)
    # print('trade_count:', trade_count, 'profit_count:', profit_count, 'loss_count:', loss_count, 'profit_sum:', profit_sum, 'loss_sum:', loss_sum, 'win_chance:', win_chance, 'p_l_ratio:', p_l_ratio)
    return trade_count, profit_count, loss_count, profit_sum, loss_sum, win_chance, p_l_ratio