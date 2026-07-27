import asyncio
import csv
from datetime import datetime
from telegram import Bot
from config import BOT_TOKEN, CHAT_ID

from data_provider import get_ohlcv, get_live_price
from indicators import add_indicators, analyze_signal
from risk_manager import calculate_trade_plan

# =========================
# ANALYZE TIMEFRAME
# =========================


def analyze_timeframe(timeframe):

    df = get_ohlcv(timeframe)

    df = add_indicators(df)

    result = analyze_signal(df)

    return result


# =========================
# FINAL AI DECISION
# =========================


def final_decision(results):

    buy = 0
    sell = 0

    for r in results:

        if "BUY" in r["signal"]:
            buy += 1

        elif "SELL" in r["signal"]:
            sell += 1

    if buy >= 2:

        return "🟢 STRONG BUY"

    elif sell >= 2:

        return "🔴 STRONG SELL"

    else:

        return "🟡 HOLD"


# =========================
# JOURNAL
# =========================


def save_history(signal, price):

    with open("trading_history.csv", "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([datetime.now(), signal, price])


# =========================
# MAIN
# =========================


async def main():

    print("\n🚀 BTC AI AGENT v13 PRO\n")

    price = get_live_price()

    m15 = analyze_timeframe("15m")
    h1 = analyze_timeframe("1h")
    h4 = analyze_timeframe("4h")

    results = [m15, h1, h4]

    decision = final_decision(results)

    plan = calculate_trade_plan(price, decision)

    print("💰 PRICE")
    print(price)

    print("\n📊 ANALYSIS\n")

    print("15M:", m15["signal"], m15["score"], "%")

    print("1H:", h1["signal"], h1["score"], "%")

    print("4H:", h4["signal"], h4["score"], "%")

    print("\n🧠 FINAL DECISION")
    print(decision)

    print("\n🎯 TRADE PLAN")

    print(plan)

    save_history(decision, price)

    print("\n📒 Journal Updated")


if __name__ == "__main__":

    asyncio.run(main())
