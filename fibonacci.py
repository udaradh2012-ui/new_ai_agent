# ==========================
# BTC AI v14
# FIBONACCI LEVELS
# ==========================


def calculate_fibonacci(df):

    high = float(df["high"].max())
    low = float(df["low"].min())
    current = float(df["close"].iloc[-1])

    diff = high - low

    fib_236 = high - diff * 0.236
    fib_382 = high - diff * 0.382
    fib_500 = high - diff * 0.500
    fib_618 = high - diff * 0.618
    fib_786 = high - diff * 0.786

    # Score based on current price location
    if current >= fib_618:
        score = 90
    elif current >= fib_500:
        score = 75
    elif current >= fib_382:
        score = 60
    else:
        score = 40

    return {
        "0.236": round(fib_236, 2),
        "0.382": round(fib_382, 2),
        "0.500": round(fib_500, 2),
        "0.618": round(fib_618, 2),
        "0.786": round(fib_786, 2),
        "score": score,
    }
