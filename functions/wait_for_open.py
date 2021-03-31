import datetime as dt
import time
import shift

def wait_for_open(trader: shift.Trader, wait):
    print("Waiting for market open")
    start_time = trader.get_last_trade_time()
    now = trader.get_last_trade_time()

    while start_time >= now:
        print('Wating at '+ str(now))
        time.sleep(wait)
        now = trader.get_last_trade_time()

    print("Market is Open at " + str(now))
    return now
