# ==========================================
# MULTI COIN AI SCANNER v2
# ==========================================


from config import COINS

from data_provider import get_ohlcv

from indicators import add_indicators, analyze_signal

from volume_analysis import analyze_volume

from support_resistance import calculate_levels

from fibonacci import calculate_fibonacci

from candlestick import detect_pattern

from ai_engine import calculate_ai_score

from market_analysis import market_strength


def scan_market():

    results = []

    print("COINS TO SCAN:", COINS)

    for coin in COINS:

        try:

            # ==============================
            # LOAD MARKET DATA
            # ==============================

            m15 = add_indicators(get_ohlcv(coin, "15m"))

            h1 = add_indicators(get_ohlcv(coin, "1h"))

            h4 = add_indicators(get_ohlcv(coin, "4h"))

            # ==============================
            # SIGNAL ANALYSIS
            # ==============================

            m15_signal = analyze_signal(m15)

            h1_signal = analyze_signal(h1)

            h4_signal = analyze_signal(h4)

            # ==============================
            # EXTRA ANALYSIS
            # ==============================

            volume = analyze_volume(m15)

            levels = calculate_levels(m15)

            fib = calculate_fibonacci(m15)

            pattern = detect_pattern(m15)

            # ==============================
            # AI SCORE
            # ==============================

            score = calculate_ai_score(
                m15_signal,
                h1_signal,
                h4_signal,
                volume["score"],
                levels["score"],
                fib["score"],
                pattern["score"],
            )

            # ==============================
            # MARKET TREND
            # ==============================

            strength = market_strength([m15_signal, h1_signal, h4_signal])

            confidence = round(score, 2)

            # ==============================
            # RISK LEVEL
            # ==============================

            if score >= 80:

                risk = "LOW"

            elif score >= 60:

                risk = "MEDIUM"

            else:

                risk = "HIGH"

            if strength["bullish"] > strength["bearish"]:

                trend = "BULLISH"

            elif strength["bearish"] > strength["bullish"]:

                trend = "BEARISH"

            else:

                trend = "NEUTRAL"

            # ==============================
            # SAVE RESULT
            # ==============================

            results.append(
                {
                    "coin": coin,
                    "signal": m15_signal["signal"],
                    "score": round(score, 2),
                    "confidence": confidence,
                    "risk": risk,
                    "trend": trend,
                }
            )

        except Exception as e:

            print(f"{coin} Error:", e)

            results.append(
                {
                    "coin": coin,
                    "signal": "ERROR",
                    "score": 0,
                    "confidence": 0,
                    "risk": "UNKNOWN",
                    "trend": "UNKNOWN",
                }
            )

    # ==============================
    # SORT BEST OPPORTUNITY FIRST
    # ==============================

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
