import ta

from config import EMA_FAST, EMA_SLOW, RSI_PERIOD

# ==========================================
# ADD INDICATORS
# ==========================================


def add_indicators(df):

    # EMA

    df["EMA20"] = ta.trend.EMAIndicator(df["close"], EMA_FAST).ema_indicator()

    df["EMA50"] = ta.trend.EMAIndicator(df["close"], EMA_SLOW).ema_indicator()

    # RSI

    df["RSI"] = ta.momentum.RSIIndicator(df["close"], RSI_PERIOD).rsi()

    # MACD

    macd = ta.trend.MACD(df["close"])

    df["MACD"] = macd.macd()

    df["MACD_SIGNAL"] = macd.macd_signal()

    df["MACD_DIFF"] = macd.macd_diff()

    # ATR VOLATILITY

    atr = ta.volatility.AverageTrueRange(
        high=df["high"], low=df["low"], close=df["close"], window=14
    )

    df["ATR"] = atr.average_true_range()

    return df


# ==========================================
# ANALYZE SIGNAL
# ==========================================


def analyze_signal(df):

    last = df.iloc[-1]

    bull_score = 0
    bear_score = 0

    # ==========================
    # EMA TREND
    # ==========================

    if last["EMA20"] > last["EMA50"]:

        bull_score += 25

    else:

        bear_score += 25

    # ==========================
    # PRICE POSITION
    # ==========================

    if last["close"] > last["EMA20"]:

        bull_score += 25

    else:

        bear_score += 25

    # ==========================
    # RSI
    # ==========================

    if last["RSI"] > 50:

        bull_score += 25

    else:

        bear_score += 25

    # ==========================
    # MACD
    # ==========================

    if last["MACD"] > 0:

        bull_score += 25

    else:

        bear_score += 25

    # ==========================
    # SIGNAL
    # ==========================

    if bull_score >= 75:

        signal = "🟢 BUY"
        confidence = bull_score

    elif bear_score >= 75:

        signal = "🔴 SELL"
        confidence = bear_score

    else:

        signal = "🟡 HOLD"
        confidence = max(bull_score, bear_score)

    return {
        "signal": signal,
        "score": confidence,
        "bull_score": bull_score,
        "bear_score": bear_score,
        "rsi": round(last["RSI"], 2),
        "price": last["close"],
        "ema20": last["EMA20"],
        "ema50": last["EMA50"],
        "macd": last["MACD"],
        "macd_diff": last["MACD_DIFF"],
        "atr": round(last["ATR"], 2),
    }
