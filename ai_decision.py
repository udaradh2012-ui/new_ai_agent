# ==========================================
# BTC AI v16
# SMART DECISION ENGINE SCALPING UPDATE
# ==========================================


def smart_decision(m15, h1, h4, ai_score):

    buy = 0
    sell = 0

    signals = [m15, h1, h4]

    for signal in signals:

        if "BUY" in signal["signal"]:
            buy += 1

        elif "SELL" in signal["signal"]:
            sell += 1

    # =====================================
    # SCALPING PRIORITY
    # 15M + 1H agreement
    # =====================================

    if "SELL" in m15["signal"] and "SELL" in h1["signal"] and ai_score >= 15:

        return "🔴 SCALP SELL"

    if "BUY" in m15["signal"] and "BUY" in h1["signal"] and ai_score >= 15:

        return "🟢 SCALP BUY"

    # =====================================
    # STRONG CONFIRMATION
    # =====================================

    if buy == 3 and ai_score >= 75:

        return "🟢 STRONG BUY"

    if sell == 3 and ai_score <= 25:

        return "🔴 STRONG SELL"

    # =====================================
    # NORMAL SIGNAL
    # =====================================

    if ai_score >= 60:

        if buy >= 2:
            return "🟢 BUY"

        elif sell >= 2:
            return "🔴 SELL"

    # =====================================
    # WEAK SIGNAL
    # =====================================

    if ai_score < 40:

        if sell >= 2:
            return "🔴 WEAK SELL"

        elif buy >= 2:
            return "🟢 WEAK BUY"

    return "🟡 HOLD"
