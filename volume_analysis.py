# ==========================
# BTC AI v14
# VOLUME ANALYSIS
# ==========================


def analyze_volume(df):

    current_volume = float(df["volume"].iloc[-1])
    average_volume = float(df["volume"].tail(20).mean())

    if current_volume >= average_volume * 1.20:
        score = 100
        status = "🟢 Very High Volume"

    elif current_volume >= average_volume:
        score = 80
        status = "🟢 High Volume"

    elif current_volume >= average_volume * 0.80:
        score = 60
        status = "🟡 Normal Volume"

    else:
        score = 30
        status = "🔴 Low Volume"

    return {
        "current": round(current_volume, 2),
        "average": round(average_volume, 2),
        "status": status,
        "score": score,
    }
