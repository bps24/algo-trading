import shift
import time
import pandas as pd
from close_positions import close_positions
from transaction_summary import transaction_summary

START_NAV = 1000000
SHARE_MULT = 100
NUM_OF_STOCKS = 30

PERIOD = 40
Z = 2.5
LAG = 15


def sma_strategy(trader: shift.Trader, ticker: str, endtime, f, state = "IN", ):

    print('Threading ' + ticker)
    f.write('Threading ' + ticker)
    now =  trader.get_last_trade_time().time()
    prices = []
    while endtime.time() > now:
        time.sleep(LAG-1)
        now = trader.get_last_trade_time().time()
        prices.append(trader.get_last_price(ticker))
        time.sleep(1)

        
        """
        if len(prices) < 31:
            if ticker == "CSCO":
                print(prices)
            continue
        """

        df = pd.DataFrame(prices[-1*PERIOD:])
        ema = float(df.ewm(com=.5).mean()[0].iloc[[-1]])
        sd = df.std()[0]
        b_upper = ema + sd * Z
        b_lower = ema - sd * Z
        cur = trader.get_last_price(ticker)
        """
        if ticker == "CSCO":
            print(ema)
            print(b_upper)
            print(b_lower)
            print(cur)
        """
        
        
        if state == "IN": ## If previously between lines
            if cur >= b_upper: ## If above upper
                amt = int((float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur)
                pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, amt)
                state = "ABOVE"
                trader.submit_order(pos)
                transaction_summary(trader, pos, f)
            elif cur <= b_lower: ## If below under
                amt = int((float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur)
                pos = shift.Order(shift.Order.Type.MARKET_SELL, ticker, amt)
                state = "BELOW"
                trader.submit_order(pos)
                transaction_summary(trader, pos, f)
        elif state == "ABOVE" and cur <= ema: ## IF previously above, but now between
            pos = shift.Order(shift.Order.Type.MARKET_SELL, ticker, int(abs(trader.get_portfolio_item(ticker).get_shares())/SHARE_MULT))
            state = "IN"
            trader.submit_order(pos)
            transaction_summary(trader, pos, f)
        elif state == "BELOW" and cur >= ema: ## If previously below, but now between
            pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, int(abs(trader.get_portfolio_item(ticker).get_shares())/SHARE_MULT))
            state = "IN"
            trader.submit_order(pos)
            transaction_summary(trader, pos, f)


    trader.cancel_all_sample_prices_requests()
    close_positions(trader, ticker)

    return