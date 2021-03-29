import sys
import time
import credentials
import numpy as np
import datetime as dt
import shift


def main(argv):
    trader = shift.Trader(credentials.user)
    try:
        trader.connect("initiator.cfg", credentials.password)
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)


    ## Let's make some money


    trader.disconnect()


if __name__ == "__main__":
    main(sys.argv)