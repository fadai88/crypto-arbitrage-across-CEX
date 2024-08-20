import ccxt
import time
import fees

def fetch_order_books(exchanges, symbol):
    order_books = {}
    for name, exchange in exchanges.items():
        try:
            order_book = exchange.fetch_order_book(symbol)
            order_books[name] = order_book
        except Exception as e:
            print(f"Error fetching order book for {name}: {e}")
    return order_books

def calculate_profit_with_fees(buy_exchange, sell_exchange, buy_price, sell_price, amount, withdrawal_fees):
    # Calculate the number of coins we can buy
    coins_bought = amount / buy_price
    
    # Subtract the withdrawal fee
    coins_after_withdrawal = coins_bought - withdrawal_fees.get(buy_exchange, 0)
    
    # Calculate the sale amount
    sale_amount = coins_after_withdrawal * sell_price
    
    # Calculate profit
    profit = sale_amount - amount
    profit_percentage = (profit / amount) * 100
    
    return profit, profit_percentage

def find_arbitrage_opportunities(order_books, initial_capital, withdrawal_fees, min_profit_percentage):
    opportunities = []
    exchange_names = list(order_books.keys())
    
    for i in range(len(exchange_names)):
        for j in range(i + 1, len(exchange_names)):
            buy_exchange = exchange_names[i]
            sell_exchange = exchange_names[j]
            
            buy_price = order_books[buy_exchange]['asks'][0][0]
            sell_price = order_books[sell_exchange]['bids'][0][0]
            
            profit, profit_percentage = calculate_profit_with_fees(
                buy_exchange, sell_exchange, buy_price, sell_price, 
                initial_capital, withdrawal_fees
            )
            
            if profit_percentage > min_profit_percentage:
                opportunities.append({
                    'buy_exchange': buy_exchange,
                    'sell_exchange': sell_exchange,
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'profit': profit,
                    'profit_percentage': profit_percentage
                })
    
    return opportunities

def main():
    exchanges = {
        'binance': ccxt.binance(),
        'huobi': ccxt.huobi(),
        'kucoin': ccxt.kucoin(),
        'gateio': ccxt.gateio(),
        'crypto-com': ccxt.cryptocom()
    }
    
    symbol = 'CHZ/USDT'
    initial_capital = 10000  # $1000 initial capital
    min_profit_percentage = 0.01  # 0.1% minimum profit
    coin = symbol[:symbol.find('/')]
    # Withdrawal fees for each exchange (in PEOPLE coins)
    withdrawal_fees = {
        'binance': fees.fetch_withdrawal_fees('binance', coin),
        'huobi': fees.fetch_withdrawal_fees('huobi', coin),
        'kucoin': fees.fetch_withdrawal_fees('kucoin', coin),
        'gateio': 88,  # Example value, please check the actual fee
        'crypto-com': fees.fetch_withdrawal_fees('crypto-com', coin)
    }
    
    while True:
        order_books = fetch_order_books(exchanges, symbol)
        opportunities = find_arbitrage_opportunities(order_books, initial_capital, withdrawal_fees, min_profit_percentage)
        
        for opportunity in opportunities:
            print(f"Arbitrage opportunity found:")
            print(f"Buy from {opportunity['buy_exchange']} at {opportunity['buy_price']}")
            print(f"Sell on {opportunity['sell_exchange']} at {opportunity['sell_price']}")
            print(f"Potential profit: ${opportunity['profit']:.2f} ({opportunity['profit_percentage']:.2f}%)")
            print("---")
        
        if not opportunities:
            print("No profitable arbitrage opportunities found.")
        
        time.sleep(10)  # Wait for 10 seconds before checking again

if __name__ == "__main__":
    main()


