# ==========================
# BTC AI v16
# ADVANCED WEIGHTED AI ENGINE
# ==========================


def calculate_ai_score(
    m15, h1, h4, volume_score=50, sr_score=50, fib_score=50, candle_score=0
):

    # =====================================
    # Timeframe Weights
    # =====================================

    m15_weight = 0.20
    h1_weight = 0.30
    h4_weight = 0.50

    timeframe_score = (
        m15["score"] * m15_weight + h1["score"] * h1_weight + h4["score"] * h4_weight
    )

    # =====================================
    # Extra Scores
    # =====================================

    extra_score = (
        volume_score * 0.15 + sr_score * 0.10 + fib_score * 0.10 + candle_score * 0.10
    )

    # =====================================
    # Final Score
    # =====================================

    final_score = timeframe_score * 0.65 + extra_score * 0.35

    return round(final_score, 2)
