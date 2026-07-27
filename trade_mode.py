def detect_trade_mode(m15, h1, h4, ai_score):

    # SCALPING SELL

    if "SELL" in m15["signal"] and "SELL" in h1["signal"] and ai_score >= 15:

        return {
            "mode": "⚡ SCALPING MODE",
            "risk": "LOW",
            "reason": "15M + 1H short trend agreement",
        }

    # SCALPING BUY

    if "BUY" in m15["signal"] and "BUY" in h1["signal"] and ai_score >= 15:

        return {
            "mode": "⚡ SCALPING MODE",
            "risk": "LOW",
            "reason": "15M + 1H long trend agreement",
        }

    return {
        "mode": "⛔ NO TRADE",
        "risk": "HIGH",
        "reason": "Insufficient confirmation",
    }
