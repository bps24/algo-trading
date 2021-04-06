import sys
import time
import credentials
#import numpy as np
import datetime as dt
import shift
import threading

sys.path.insert(1, './functions')
from portfolio_summary import portfolio_summary
from close_positions import close_positions
from sma_strategy import sma_strategy
from wait_for_open import wait_for_open
from summary_thread import summary_thread

def main(argv):
    
    #Connect and Login
    trader = shift.Trader(credentials.user)
    try:
        trader.connect("initiator.cfg", credentials.password)
        print("Connected")
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)


    time.sleep(10)
    lag = 2

    today_date = trader.get_last_trade_time().date()
    start_time = dt.time(9,31,0)
    start = dt.datetime.combine(today_date,start_time)
    time.sleep(5)


    print("START ", start)
    wait_for_open(trader,start,lag)
    end = dt.datetime.combine(today_date,dt.time(15,45,0))
    print("END ", end)
    close_positions(trader)
    portfolio_summary(trader)
    
    threads = []
    for item in trader.get_stock_list():
        strat = threading.Thread(target=sma_strategy, args=[trader,item,end])
        threads.append(strat)

    port = threading.Thread(target=summary_thread, args=[trader, end])
    threads.append(port)
    print("ALL THREADS CREATED")

    for strat in threads:
        strat.start()
        time.sleep(1)

    print("ALL THREADS STARTED")

    time.sleep(10)
    for strat in threads:
        strat.join()

    print("ALL THREADS JOINED")

    time.sleep(50)

    print("CLOSING UP SHOP")

    close_positions(trader)
    time.sleep(50)
    
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()


if __name__ == "__main__":
    main(sys.argv)