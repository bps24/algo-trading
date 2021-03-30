import sys
import time
import credentials
import numpy as np
import datetime as dt
import shift


def main(argv):
    trader = shift.Trader("democlient")
    try:
<<<<<<< Updated upstream
        trader.connect(credentials.user, credentials.password)
=======
        trader.connect("initiator.cfg", "password")
>>>>>>> Stashed changes
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)


    aapl_mb = shift.Order(shift.Order.Type.MARKET_BUY, "AAPL", 1)
    trader.submit_order(aapl_mb)
    print('trade completed')

    time.sleep(200)

    trader.disconnect()




if __name__ == "__main__":
    main(sys.argv)