# ==========================================
# ENTRY QUALITY SYSTEM
# ==========================================


def calculate_entry_quality(
    final_signal,
    pullback_signal,
    volume_score,
    atr,
    price,
    support,
    resistance,
    ema20,
    ema50,
):

    # Pullback
    pullback_points = 25 if pullback_signal else 0

    # Volume

    if volume_score >= 90:

        volume_points = 20

    elif volume_score >= 70:

        volume_points = 15

    elif volume_score >= 50:

        volume_points = 10

    else:

        volume_points = 0

    # ATR

    atr_points = 0

    if price > 0:

        atr_percent = (atr / price) * 100

    else:

        atr_percent = 0

    if atr_percent >= 0.15:

        atr_points = 15

    elif atr_percent >= 0.08:

        atr_points = 10

    # Support Resistance

    sr_points = 0

    if "BUY" in final_signal:

        distance = resistance - price

        if distance > atr:

            sr_points = 15

        elif distance > 0:

            sr_points = 10

    elif "SELL" in final_signal:

        distance = price - support

        if distance > atr:

            sr_points = 15

        elif distance > 0:

            sr_points = 10

    # Trend

    trend_points = 0

    if "BUY" in final_signal and ema20 > ema50:

        trend_points = 15

    elif "SELL" in final_signal and ema20 < ema50:

        trend_points = 15

    # Total

    total = pullback_points + volume_points + atr_points + sr_points + trend_points

    if total >= 80:

        status = "🟢 EXCELLENT"

    elif total >= 65:

        status = "🟡 GOOD"

    elif total >= 50:

        status = "🟠 WEAK"

    else:

        status = "🔴 SKIP"

    return {
        "score": total,
        "status": status,
        "pullback": pullback_points,
        "volume": volume_points,
        "atr": atr_points,
        "sr": sr_points,
        "trend": trend_points,
    }
