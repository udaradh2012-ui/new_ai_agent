# ==========================
# BTC AI v14
# MARKET STRENGTH ANALYSIS
# ==========================


def market_strength(results):

    bullish = 0
    bearish = 0
    neutral = 0

    for data in results:

        if data["score"] >= 75:
            bullish += 1

        elif data["score"] <= 25:
            bearish += 1

        else:
            neutral += 1

    total = len(results)

    if total == 0:
        return {"bullish": 0, "bearish": 0, "neutral": 0}

    return {
        "bullish": round(bullish / total * 100, 1),
        "bearish": round(bearish / total * 100, 1),
        "neutral": round(neutral / total * 100, 1),
    }
