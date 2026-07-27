# ==========================================
# BTC AI v16
# CANDLESTICK PATTERN ENGINE
# ==========================================


def detect_pattern(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    open_price = last["open"]
    close_price = last["close"]
    high = last["high"]
    low = last["low"]

    body = abs(close_price - open_price)
    candle_range = high - low

    # -----------------------------
    # DOJI
    # -----------------------------
    if body <= candle_range * 0.10:
        return {"pattern": "DOJI", "signal": "NEUTRAL", "score": 0}

    # -----------------------------
    # BULLISH ENGULFING
    # -----------------------------
    if (
        prev["close"] < prev["open"]
        and close_price > open_price
        and close_price > prev["open"]
        and open_price < prev["close"]
    ):

        return {"pattern": "BULLISH ENGULFING", "signal": "BUY", "score": 20}

    # -----------------------------
    # BEARISH ENGULFING
    # -----------------------------
    if (
        prev["close"] > prev["open"]
        and close_price < open_price
        and open_price > prev["close"]
        and close_price < prev["open"]
    ):

        return {"pattern": "BEARISH ENGULFING", "signal": "SELL", "score": 20}

    return {"pattern": "NONE", "signal": "NEUTRAL", "score": 0}
