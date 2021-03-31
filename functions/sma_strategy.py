import shift
import time
import pandas as pd
from close_positions import close_positions
from transaction_summary import transaction_summary

START_NAV = 1000000
SHARE_MULT = 100
NUM_OF_STOCKS = 30


def sma_strategy(trader: shift.Trader, ticker: str, enter, endtime):

    print('Threading ' + ticker)
    now =  trader.get_last_trade_time().time()
    while endtime > now:
        time.sleep(5)
        now =  trader.get_last_trade_time().time()
        prices = pd.Series(trader.get_sample_prices(ticker, True))
        time.sleep(1)

        sma = prices[:19].mean()
        #print(sma)
        b_upper = sma + (prices[:19].std() * 2.0)
        b_lower = sma - (prices[:19].std() * 2.0)

        cur = trader.get_close_price(ticker, True, 1)
        cur2 = trader.get_close_price(ticker, False, 1)

        if enter:
            if cur >= b_upper:
                amt = (float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur
                pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, amt)
                enter = False
                trader.submit_order(pos)
                transaction_summary(pos)
            elif cur2 <= b_lower:
                amt = (float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur2
                pos = shift.Order(shift.Order.Type.MARKEY_SELL, ticker, amt)
                enter = False
                trader.submit_order(pos)
                transaction_summary(pos)
        else:
            if cur2 <= b_upper:
                pos = shift.Order(shift.Order.Type.MARKET_SELL, ticker, amt)
                enter = True
                trader.submit_order(pos)
                transaction_summary(pos)
            elif cur >= b_lower:
                pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, amt)
                enter = True
                trader.submit_order(pos)
                transaction_summary(pos)

    trader.cancel_all_sample_prices_requests()
    close_positions(trader, ticker)

    return