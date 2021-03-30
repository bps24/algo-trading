import sys
import time
import credentials
#import numpy as np
import datetime as dt
import shift

sys.path.insert(1, './functions')
from portfolio_summary import portfolio_summary
from close_positions import close_positions


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

    #TODO Create for loop that implements sma thread for each stock 

    #TODO Create a loop that creates threads that manaages liquidity / capital for each stock 

    #TODO Begin closing positions at 3:50

    trader.disconnect()




if __name__ == "__main__":
    main(sys.argv)