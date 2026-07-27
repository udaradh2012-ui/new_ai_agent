# ==========================================
# AI QUALITY SCORE
# ==========================================


def calculate_ai_quality(stats):

    # ==============================
    # SIGNAL ACCURACY
    # ==============================

    if stats["trades"] > 0:

        signal_accuracy = (stats["wins"] / stats["trades"]) * 100

    else:

        signal_accuracy = 0

    # ==============================
    # RISK MANAGEMENT
    # ==============================

    drawdown = stats.get("max_drawdown", 0)

    if drawdown < 5:

        risk_score = 100

    elif drawdown < 10:

        risk_score = 80

    elif drawdown < 20:

        risk_score = 60

    else:

        risk_score = 40

    # ==============================
    # TRADE DISCIPLINE
    # ==============================

    if stats["trades"] > 0:

        discipline = 100

    else:

        discipline = 0

    # ==============================
    # OVERALL SCORE
    # ==============================

    overall = signal_accuracy * 0.5 + risk_score * 0.3 + discipline * 0.2

    if overall >= 90:

        grade = "A+"

    elif overall >= 80:

        grade = "A"

    elif overall >= 70:

        grade = "B"

    elif overall >= 60:

        grade = "C"

    else:

        grade = "D"

    return {
        "signal_accuracy": round(signal_accuracy, 2),
        "risk_management": risk_score,
        "trade_discipline": discipline,
        "overall": round(overall, 2),
        "grade": grade,
    }
