import datetime as dt
import time
import shift

def wait_for_open(trader: shift.Trader, start_time, wait, f):
    print("Waiting for market open")
    f.write("Waiting for market open")

    now = trader.get_last_trade_time()

    while start_time >= now:
        print('Wating at '+ str(now))
        f.write('Waiting at ' + str(now))

        time.sleep(wait)
        now = trader.get_last_trade_time()

    print("Market is Open at " + str(now))
    f.write("Market is Open at " + str(now))
    return now
