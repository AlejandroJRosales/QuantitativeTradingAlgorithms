import yfinance as yf
import talib
import numpy as np
import datetime


key = 'enter-api-key'
period = "6mo"


def get_high_low_close(stock):
    high_low_close = dict()
    ticker = yf.Ticker(stock)
    high_low_close['high'] = np.array([close for close in ticker.history(period=period)["Close"]])
    high_low_close['low'] = np.array([high for high in ticker.history(period=period)["High"]])
    high_low_close['close'] = np.array([low for low in ticker.history(period=period)["Low"]])

    return high_low_close


def volatile_algo(stock, hist):
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
    if (80 < slowk < 100 or 80 < slowd < 95) or (-5 < macd < 5):
    # if slowk > 90 or slowd > 90:
        print(f"Sell {stock}")
        # order_target(stock, 0)

    elif (rsi < 30) or (0 < slowk < 20 or 0 < slowd < 20) or (-5 < macd < 5):
    # elif slowk < 10 or slowd < 10:
        print(f"Buy {stock}")
        # order_target_percent(stock, long_pct_per_stock)

    else:
        print(f"Hold {stock}")


def nonvolatile_algo(stock, hist):
    # Create the MACD signal and pass in the three parameters: fast period, slow period, and the signal.
    macd_raw, signal, hist2 = talib.MACD(hist['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    print(talib.MACD(hist['close'], fastperiod=12, slowperiod=26, signalperiod=9))
    macd = macd_raw[-1] - signal[-1]

    # print([macd_raw[day] - signal[day] for day in range(len(signal) - 2, len(signal))])
    # gap_up = any([True if macd_raw[day] - signal[day] > 0 and macd_raw[day  + 1] - signal[day + 1] < 0 else False for day in range(len(signal) - 2, len(signal) - 1)])
    # gap_down = any([True if macd_raw[day] - signal[day] < 0 and macd_raw[day  + 1] - signal[day + 1] > 0 else False for day in range(len(signal) - 2, len(signal) - 1)])

    # gap_up = macd_raw[-2] - signal[-2] < 0 and macd_raw[-1] - signal[-1] > 0
    # print(signal[-2], signal[-1])
    # gap_down = macd_raw[-2] - signal[-2] > 0 and macd_raw[-1] - signal[-1] < 0

    if macd < 0:
        print(f"Sell {stock}")
        # order_target(stock, 0)

    elif macd > 0:
        print(f"Buy {stock}")
        # order_target_percent(stock, long_pct_per_stock)

    else:
        print(f"Hold {stock}")


def main():
    tickers = ['PYPL']
    # tickers = ['APPN', 'GMED', 'CRWD', 'GOOG', 'SQ', 'PYPL', 'ZNGA', 'ABBV', 'TREX']
    print('Volatile Algorithm Says:')

    # for ticker in tickers:
    #     hist = get_high_low_close(ticker)
    #     volatile_algo(ticker, hist)

    print('\n\nNonvolatile Algorithm Says:')
    for ticker in tickers:
        hist = get_high_low_close(ticker)
        nonvolatile_algo(ticker, hist)


if __name__ == '__main__':
    main()
