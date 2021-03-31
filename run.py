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

    lag = 1
    today = wait_for_open(trader,lag).date()
    end_time = dt.datetime.combine(today,dt.time(23,30,0))
    print("ENDTIME ", end_time)
    
    threads = []
    for item in trader.get_stock_list():

        strat = threading.Thread(target=sma_strategy, args=[trader,item,end_time])
        threads.append(strat)

    for strat in threads:
        strat.start()
        time.sleep(1)

    time.sleep(10)
    for strat in threads:
        strat.join()
    
    close_positions(trader)

    trader.disconnect()


if __name__ == "__main__":
    main(sys.argv)