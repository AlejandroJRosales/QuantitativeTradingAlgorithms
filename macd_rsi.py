import requests
import talib
import numpy as np

key = 'Enter APY Key Here'

def get_price_history(**kwargs):

    url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(kwargs.get('symbol'))

    params = {}
    params.update({'apikey': key})

    for arg in kwargs:
        parameter = {arg: kwargs.get(arg)}
        params.update(parameter)

    return requests.get(url, params=params).json()


def get_high_low_close(price_history):
    high_low_close = {}
    high_low_close['high'] = np.array([data['high'] for data in price_history['candles']])
    high_low_close['low'] = np.array([data['low'] for data in price_history['candles']])
    high_low_close['close'] = np.array([data['close'] for data in price_history['candles']])
    return high_low_close


def rebalance(stock, hist):
    # # Create the MACD signal and pass in the three parameters: fast period, slow period, and the signal.
    macd_raw, signal, hist2 = talib.MACD(hist['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    macd = macd_raw[-1] - signal[-1]

    rsi = talib.RSI(hist['close'], timeperiod=14)[-1]

    slowk, slowd = talib.STOCH(hist['high'],
                               hist['low'],
                               hist['close'],
                               fastk_period=5,
                               slowk_period=3,
                               slowk_matype=0,
                               slowd_period=3,
                               slowd_matype=0)

    # get the most recent value
    slowk = slowk[-1]
    slowd = slowd[-1]

    print("You should", end=" ")
    if (slowk > 90 or slowd > 90) or macd < 0:
        print(f"sell {stock}")
        # order_target(stock, 0)

    elif rsi < 30 or (slowk < 10 or slowd < 10) or macd > 0:
        print(f"buy {stock}")
        # order_target_percent(stock, long_pct_per_stock)

    else:
        print(f"hold current shares of {stock}")


tickers = ['APPN', 'GMED']
for ticker in tickers:
    price_history = get_price_history(symbol=ticker, period=1, periodType='day', frequencyType='minute')
    hist = get_high_low_close(price_history)
    rebalance(ticker, hist)
