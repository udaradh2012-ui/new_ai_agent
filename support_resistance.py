# ==========================
# BTC AI v14
# SUPPORT / RESISTANCE
# ==========================


def calculate_levels(df):

    support = float(df["low"].tail(50).min())
    resistance = float(df["high"].tail(50).max())

    current_price = float(df["close"].iloc[-1])

    if current_price <= support * 1.01:
        score = 90

    elif current_price >= resistance * 0.99:
        score = 40

    else:
        score = 70

    return {
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "score": score,
    }
