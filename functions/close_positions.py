import shift

def close_positions(trader: shift.Trader, ticker: str = "ALL", f=None):
    if ticker == "ALL":
        trader.cancel_all_pending_orders()
        for item in trader.get_portfolio_items():
            close_positions(trader, item, f)

    elif ticker == "SHORT":
        for item in trader.get_portfolio_items().values():
            if item.get_shares() < 0:
                close_positions(trader, item.get_symbol())

    elif ticker == "LONG":
        for item in trader.get_portfolio_items().values():
            if item.get_shares() > 0:
                close_positions(trader, item.get_symbol())

    else:
        item = trader.get_portfolio_item(ticker)
        if item.get_shares() > 0:
            close_long = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), int(item.get_shares() / 100))
            trader.submit_order(close_long)
        elif item.get_shares() < 0:
            cover_short = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), int(item.get_shares() / -100))
            trader.submit_order(cover_short)
        print("All", ticker, "positions exited")
        f.write("All " + str(ticker) + " positions exited")