import shift

def transaction_summary(trader: shift.Trader, order: shift.Order):
    print(f"Order: {order.id}, Symbol: {order.symbol}, Type: {order.type}, Price: {order.price}, Size: {order.size}")
    return