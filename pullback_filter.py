# ==========================================
# SMART PULLBACK FILTER v2
# ==========================================


def detect_pullback(df, signal):

    try:

        close = df["close"].iloc[-1]

        previous_close = df["close"].iloc[-2]

        ema20 = df["EMA20"].iloc[-1]

        ema50 = df["EMA50"].iloc[-1]

        pullback = False

        # ==========================
        # BUY PULLBACK
        # ==========================

        if "BUY" in signal:

            trend_up = ema20 > ema50

            near_ema = abs(close - ema20) / close < 0.008

            bullish_recovery = close >= previous_close

            if trend_up and near_ema and bullish_recovery:

                pullback = True

        # ==========================
        # SELL PULLBACK
        # ==========================

        elif "SELL" in signal:

            trend_down = ema20 < ema50

            near_ema = abs(close - ema20) / close < 0.008

            bearish_recovery = close <= previous_close

            if trend_down and near_ema and bearish_recovery:

                pullback = True

        return pullback

    except Exception:

        return False
