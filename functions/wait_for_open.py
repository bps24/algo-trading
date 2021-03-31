import datetime as dt
import time
import shift

def wait_for_open(trader: shift.Trader, start_time, wait):
    now = trader.get_last_trade_time()

    while start_time > now:
        print('Wating at'+ str(now))
        time.sleep(wait)

    print("Market is Open at " + str(now))
    return True
