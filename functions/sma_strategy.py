import shift
import time
import pandas as pd
from close_positions import close_positions
from transaction_summary import transaction_summary

START_NAV = 1000000
SHARE_MULT = 100
NUM_OF_STOCKS = 30


def sma_strategy(trader: shift.Trader, ticker: str, endtime, state = "IN"):

    print('Threading ' + ticker)
    now =  trader.get_last_trade_time().time()
    while endtime > now:
        time.sleep(5)
        now =  trader.get_last_trade_time().time()
        prices = pd.Series(trader.get_sample_prices(ticker, True))
        time.sleep(1)

        sma = prices[-20:].mean()
        b_upper = sma + (prices[:19].std() * 2.0)
        b_lower = sma - (prices[:19].std() * 2.0)

        cur = trader.get_close_price(ticker, True, 1)
        cur2 = trader.get_close_price(ticker, False, 1)
        
        if state == "IN": ## If previously between lines
            if cur >= b_upper: ## If above upper
                amt = int((float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur)
                pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, amt)
                state = "ABOVE"
                trader.submit_order(pos)
                transaction_summary(trader, pos)
            elif cur2 <= b_lower: ## If below under
                amt = int((float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur2)
                pos = shift.Order(shift.Order.Type.MARKEY_SELL, ticker, amt)
                state = "BELOW"
                trader.submit_order(pos)
                transaction_summary(trader, pos)
        elif state == "ABOVE" and cur2 <= b_upper: ## IF previously above, but now between
            pos = shift.Order(shift.Order.Type.MARKET_SELL, ticker, abs(trader.get_portfolio_item(ticker).get_shares()))
            state = "IN"
            trader.submit_order(pos)
            transaction_summary(trader, pos)
        elif state == "BELOW" and cur >= b_lower: ## If previously below, but now between
            pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, abs(trader.get_portfolio_item(ticker).get_shares()))
            state = "IN"
            trader.submit_order(pos)
            transaction_summary(trader, pos)


    trader.cancel_all_sample_prices_requests()
    close_positions(trader, ticker)

    return