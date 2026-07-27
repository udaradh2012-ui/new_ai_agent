# ==========================================
# BTC AI v16
# AI REASON ENGINE
# ==========================================


def generate_reason(m15, h1, h4, volume, pattern, strength, ai_score, decision):

    reasons = []

    reasons.append(f"15M : {m15['signal']} ({m15['score']}%)")

    reasons.append(f"1H : {h1['signal']} ({h1['score']}%)")

    reasons.append(f"4H : {h4['signal']} ({h4['score']}%)")

    reasons.append(f"Volume : {volume['status']}")

    reasons.append(f"Candlestick : {pattern['pattern']}")

    reasons.append(
        f"Market Strength : "
        f"Bull {strength['bullish']}% | "
        f"Bear {strength['bearish']}%"
    )

    reasons.append(f"AI Score : {ai_score}%")

    reasons.append(f"Decision : {decision}")

    return reasons
