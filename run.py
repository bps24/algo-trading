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

def main(argv):
    
    #Connect and Login
    trader = shift.Trader(credentials.user)
    try:
        trader.connect("initiator.cfg", credentials.password)
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    today = trader.get_last_trade_time().date()
    startTime = dt.time(9,30,00)
    wait_for_open(trader,dt.datetime.combine(today,startTime),1)
    endtime = dt.time(15,50,00)

    threads = []
    for item in trader.get_stock_list():
        strat = threading.Thread(target=sma_strategy, args=[trader,item,endtime])
        threads.append(strat)

    time.sleep(10)
    for strat in threads:
        strat.start()

    time.sleep(10)
    for strat in threads:
        strat.join()
    
    close_positions(trader)

    trader.disconnect()


if __name__ == "__main__":
    main(sys.argv)