import ccxt
import pandas as pd

from config import SYMBOL, COINS

exchange = ccxt.binance()


def get_ohlcv(symbol, timeframe, limit=200):

    candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    df = pd.DataFrame(
        candles, columns=["time", "open", "high", "low", "close", "volume"]
    )

    df["time"] = pd.to_datetime(df["time"], unit="ms")

    return df


def get_live_price(symbol):

    ticker = exchange.fetch_ticker(symbol)

    return ticker["last"]


def get_24h_change(symbol):

    ticker = exchange.fetch_ticker(symbol)

    return ticker["percentage"]


def get_volume(symbol=SYMBOL):

    ticker = exchange.fetch_ticker(symbol)

    return ticker["quoteVolume"]
