import shift
import time
from portfolio_summary import portfolio_summary

def summary_thread(trader: shift.Trader, endtime):
    print('Threading Summary')
    now = trader.get_last_trade_time().time()
    while endtime.time() > now:
        time.sleep(60)
        portfolio_summary(trader)