from binance.client import Client
from binance.exceptions import BinanceAPIException
import time

api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_SECRET_KEY'
client = Client(api_key, api_secret)

def get_btc_price():
    try:
        ticker = client.get_symbol_ticker(symbol='BTCUSDT')
        return float(ticker['price'])
    except BinanceAPIException as e:
        print(f"Грешка при получаване на цената: {e}")
        return None

def get_balance(asset):
    try:
        balance = client.get_asset_balance(asset=asset)
        return float(balance['free'])
    except BinanceAPIException as e:
        print(f"Грешка при проверка на баланса за {asset}: {e}")
        return None

def trading_bot():
    buy_price = 30000  
    sell_price = 35000 
    trade_count = 0    

    while True:
        current_price = get_btc_price()
        if current_price is None:
            print("Неуспешно получаване на цена. Опитваме отново след малко.")
            time.sleep(10)
            continue

        btc_balance = get_balance('BTC')
        usdt_balance = get_balance('USDT')

        if current_price <= buy_price and usdt_balance is not None and usdt_balance >= 10:
            quantity = round(usdt_balance / current_price, 6)
            try:
                print(f"Опит за покупка на {quantity} BTC на цена {current_price} USDT")
                # client.order_market_buy(symbol='BTCUSDT', quantity=quantity)
                print("Успешно купихме BTC.")
                trade_count += 1
            except BinanceAPIException as e:
                print(f"Грешка при покупка на BTC: {e}")

        elif current_price >= sell_price and btc_balance is not None and btc_balance > 0.0001:
            try:
                print(f"Опит за продажба на {btc_balance} BTC на цена {current_price} USDT")
                # client.order_market_sell(symbol='BTCUSDT', quantity=btc_balance)
                print("Успешно продадохме BTC.")
                trade_count += 1
            except BinanceAPIException as e:
                print(f"Грешка при продажба на BTC: {e}")

        if trade_count >= 5:
            print("Достигнат е лимитът от 5 сделки. Прекратяване на бота.")
            break

        time.sleep(10)

trading_bot()
