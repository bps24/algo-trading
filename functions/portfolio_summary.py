import shift
import time

def portfolio_summary(trader: shift.Trader):


    """Prints a snapshot of the portfolio performance and holdings"""
    print("--------------------------------Portfolio Summary--------------------------------")
    print(
        "%12s%12s%9s%26s"
        % ("Buying Power\t", "Total Shares\t","Total P&L\t", "Timestamp"))
    print(
        "%12.2f\t%12d\t%9.2f\t%26s"
        % (
            trader.get_portfolio_summary().get_total_bp(),
            trader.get_portfolio_summary().get_total_shares(),
            trader.get_portfolio_summary().get_total_realized_pl(),
            trader.get_portfolio_summary().get_timestamp(),
        )
    )

    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(
        "%6s%6s%10s%14s%10s%26s"
        % ("Symbol\t", "Shares\t", "Price\t", "Total Value\t", "P&L\t","Timestamp"))
    for holding in trader.get_portfolio_items().values():
        print(
            "%6s\t%6d\t%9.2f\t%13.2f\t%9.2f\t%26s"
            % (
                holding.get_symbol(),
                holding.get_shares(),
                holding.get_price(),
                holding.get_shares() * holding.get_price(),
                holding.get_realized_pl(),
                holding.get_timestamp(),
            )
        )

    print("---------------------------------------------------------------------------------")

    return
