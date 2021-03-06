from binance.client import Client
import time
import datetime

api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

def bot(target):
    bot_1min(target)
    bot_5min(target)

def bot_1min(target):
    buy_multiplier = 5.5
    sell_multiplier = 5

    avg_data = moving_24h_data(target)
    curr_data = most_recent_data(target, "1min")

    if avg_data[1] < 0:
        buy_multiplier = 8
        sell_multiplier = 6
    
    avg_1min_vol = avg_data[0] / 24 / 60
    # avg_1min_change = avg_data[1] / 24 / 60

    curr_1min_vol = curr_data[0]
    curr_1min_change = curr_data[1]

    if curr_1min_vol >= avg_1min_vol * buy_multiplier and curr_1min_change > 0:
        print("1 min bot @ "+ str(datetime.datetime.now()) + ": vol " + str(curr_1min_vol) + ", avg vol " + str(avg_1min_vol))
        all_in(target)
        
    if curr_1min_vol >= avg_1min_vol * sell_multiplier and curr_1min_change < 0: 
        print("1 min bot @ "+ str(datetime.datetime.now()) + ": vol " + str(curr_1min_vol) + ", avg vol " + str(avg_1min_vol))
        all_out(target)

def bot_5min(target):
    buy_multiplier = 5
    sell_multiplier = 4

    avg_data = moving_24h_data(target)
    curr_data = moving_5min_data(target)

    if avg_data[1] < 0:
        buy_multiplier = 6
        sell_multiplier = 5
    
    avg_5min_vol = avg_data[0] / 24 / 60 * 5
    # avg_5min_change = avg_data[1] / 24 / 60 * 5

    curr_5min_vol = curr_data[0]
    curr_5min_change = curr_data[1]

    if curr_5min_vol >= avg_5min_vol * buy_multiplier and curr_5min_change > 0.25:
        print("5 min bot @ "+ str(datetime.datetime.now()) + ": vol " + str(curr_5min_vol) + ", avg vol " + str(avg_5min_vol))
        all_in(target)
              
    if curr_5min_vol >= avg_5min_vol * sell_multiplier and curr_5min_change < -0.20:
        print("5 min bot @ "+ str(datetime.datetime.now()) + ": vol " + str(curr_5min_vol) + ", avg vol " + str(avg_5min_vol)) 
        all_out(target)
              
# this is stupid
def most_recent_data(target, time_interval):
    if time_interval == "1min":
        interval_ = Client.KLINE_INTERVAL_1MINUTE
    if time_interval == "5min":
        interval_ = Client.KLINE_INTERVAL_5MINUTE
    if time_interval == "1day":
        interval_ = Client.KLINE_INTERVAL_1DAY
    
    candles = client.get_klines(symbol=target, interval=interval_,limit = 1)

    time = candles[0]
    
    open_ = float(time[1])
    high = float(time[2])
    low = float(time[3])
    close = float(time[4])
    volume = float(time[5])

    change = (close - open_)/open_ * 100


    return (volume, change)

def moving_5min_data(target):
    
    candles = client.get_klines(symbol=target, interval= Client.KLINE_INTERVAL_1MINUTE,limit = 5)

    open_ = float(candles[0][1])
    close = float(candles[4][4])
    change = (close - open_)/open_ * 100

    total_vol = 0.0

    for candle in candles:
        total_vol += float(candle[5])

    return (total_vol, change)
    
    

def moving_24h_data(target):
    data = client.get_ticker(symbol = target)

    change = float(data["priceChangePercent"])
    volume = float(data["volume"])

    return (volume, change)

def all_in(target):
    
    balance = float(client.get_asset_balance(asset='USDT')["free"])
    market_price = float(client.get_order_book(symbol=target, limit=5)['asks'][0][0])
    quantity_ = round(balance/market_price,6) - 0.000001
   
    if quantity_ > 0.000001:
        order = client.order_market_buy(symbol='BTCUSDT',quantity=quantity_)
        print("Bought " + str(quantity_) + " " + target + " @ " + str(market_price))
    else:
        print("Tried to buy " + str(quantity_) + " " + target + " @ " + str(market_price))

    print("==================================================")

def all_out(target):
    
    balance = float(client.get_asset_balance(asset='BTC')["free"])
    market_price = float(client.get_order_book(symbol=target, limit=5)['bids'][0][0])
    quantity_ = round(balance, 6) - 0.000001

    if quantity_ > 0.000001:
        order = client.order_market_sell(symbol='BTCUSDT',quantity=quantity_)
        print("Sold " + str(quantity_) + " " + target + " @ " + str(market_price))
    else:
        print("Tried to sell " + str(quantity_) + " " + target + " @ " + str(market_price))

    print("==================================================")
    
if __name__ == '__main__':
    coin1 = 'BTC'
    coin2 = 'USDT'
    target = 'BTCUSDT'
    
    while True:
        bot(target)
        time.sleep(11)
        
