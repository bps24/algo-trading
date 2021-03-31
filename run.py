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


def main(argv):
    
    #Connect and Login
    trader = shift.Trader(credentials.user)
    try:
        trader.connect("initiator.cfg", credentials.password)
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)


    #TODO Wait Until Trading Starts

    threads = []
    for item in trader.get_stock_list():
        print(item)
        strat = threading.Thread(target=sma_strategy, args=[trader,item])
        threads.append(strat)

    
    #TODO Create a loop that creates threads that manaages liquidity / capital for each stock 
    for strat in threads:
        strat.start()

    for strat in threads:
        strat.join()
    
    

    
    #TODO Begin closing positions at 3:50
    close_positions(trader)

    trader.disconnect()




if __name__ == "__main__":
    main(sys.argv)