import shift
import time
import pandas as pd
from close_positions import close_positions
from transaction_summary import transaction_summary

START_NAV = 1000000
SHARE_MULT = 100
NUM_OF_STOCKS = 30


def ema_strategy(trader: shift.Trader, ticker: str, endtime, state = "BELOW"):
    """Enter long positions and exit short posistions
        when the price crosses above exponential moving average. Exit
        long positions and enter short positions when price crosses
        below exponential moving average."""


    print('Threading ' + ticker)
    now =  trader.get_last_trade_time().time()
    prices = []
    while endtime.time() > now:
        time.sleep(1)
        now = trader.get_last_trade_time().time()
        prices.append(trader.get_last_price(ticker))
        time.sleep(1)

        df = pd.DataFrame(prices[-30:])
        ema = float(df.ewm(com=.5).mean()[0].iloc[[-1]])

        cur = trader.get_last_price(ticker)

        if state == "BELOW": #Price currently below ema
            if cur > ema: #Price crosses above ema
                state = "ABOVE"
                if trader.get_portfolio_item(ticker).get_shares() != 0:
                    #Exit short positions if we have any
                    pos = shift.Order(shift.Order.Type.MARKET_SELL, ticker, int(abs(trader.get_portfolio_item(ticker).get_shares())/100))
                    trader.submit_order(pos)
                    transaction_summary(trader, pos)
                
                #Enter long position
                amt = int((float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur)
                pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, amt)
                trader.submit_order(pos)
                transaction_summary(trader, pos)

        if state == "ABOVE": #Price currently above ema
            if cur < ema: #Price crosses below ema
                state = "BELOW"
                if trader.get_portfolio_item(ticker).get_shares() != 0:
                    #Exit long positions if we have any
                    pos = shift.Order(shift.Order.Type.MARKET_BUY, ticker, int(abs(trader.get_portfolio_item(ticker).get_shares())/100))
                    trader.submit_order(pos)
                    transaction_summary(trader, pos)
                
                #Enter short position
                amt = int((float(trader.get_portfolio_summary().get_total_realized_pl()) + START_NAV) / NUM_OF_STOCKS / SHARE_MULT / cur)
                pos = shift.Order(shift.Order.Type.MARKET_SELL, ticker, amt)
                trader.submit_order(pos)
                transaction_summary(trader, pos)

    trader.cancel_all_sample_prices_requests()
    close_positions(trader, ticker)

    return