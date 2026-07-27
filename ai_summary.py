# ==========================
# BTC AI v14
# AI MARKET SUMMARY
# ==========================


def generate_summary(m15, h1, h4, levels, fib_levels):

    if m15["score"] >= 75 and h1["score"] >= 75 and h4["score"] >= 75:
        trend = "Strong Bullish"

    elif m15["score"] <= 25 and h1["score"] <= 25 and h4["score"] <= 25:
        trend = "Strong Bearish"

    else:
        trend = "Neutral"

    summary = f"""
### 📋 AI MARKET SUMMARY

• Overall Trend : {trend}

• 15M Score : {m15['score']}%

• 1H Score : {h1['score']}%

• 4H Score : {h4['score']}%

• Support : ${levels['support']}

• Resistance : ${levels['resistance']}

• Fibonacci 0.618 : ${fib_levels['0.618']}

⚠️ This analysis is for educational purposes and is not financial advice.
"""

    return summary
