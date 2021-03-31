import shift
import time

def sma_strategy(trader: shift.Trader, ticker: str, endtime):

    print('Threading ' + ticker)
    now =  trader.get_last_trade_time()
    while endtime > now:
        time.sleep(5)
        now =  trader.get_last_trade_time()
    return