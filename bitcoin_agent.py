import ccxt
import pandas as pd
import asyncio
import csv
from datetime import datetime

from telegram import Bot

from indicators import add_indicators, calculate_ai_score, market_signal

# ==========================
# TELEGRAM
# ==========================

BOT_TOKEN = "8940256279:AAFqRqtEyIKhxqeQbO7Qm3aSlHfVLlHbjHQ"
CHAT_ID = 8265070249

bot = Bot(token=BOT_TOKEN)


# ==========================
# BINANCE
# ==========================

exchange = ccxt.binance()


# ==========================
# MARKET DATA
# ==========================


def get_market(timeframe):

    candles = exchange.fetch_ohlcv("BTC/USDT", timeframe=timeframe, limit=200)

    df = pd.DataFrame(
        candles, columns=["time", "open", "high", "low", "close", "volume"]
    )

    df = add_indicators(df)

    latest = df.iloc[-1]

    score = calculate_ai_score(latest)

    signal = market_signal(score)

    price = latest["close"]

    return {
        "price": price,
        "rsi": latest["RSI"],
        "ema20": latest["EMA20"],
        "ema50": latest["EMA50"],
        "macd": latest["MACD"],
        "score": score,
        "signal": signal,
        "volume": latest["volume"],
    }


# ==========================
# RISK MANAGEMENT
# ==========================


def risk_management(price, signal):

    if "BUY" in signal:

        stop_loss = price * 0.98
        take_profit = price * 1.04

    elif "SELL" in signal:

        stop_loss = price * 1.02
        take_profit = price * 0.96

    else:

        stop_loss = 0
        take_profit = 0

    return stop_loss, take_profit


# ==========================
# JOURNAL
# ==========================


def save_trade(signal, price):

    def save_trade(signal, price):

        with open("trading_history.csv", "a", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([datetime.now(), signal, price])


# ==========================
# MAIN AI
# ==========================


async def main():

    print("\n🚀 BTC AI AGENT v12 PRO")

    m15 = get_market("15m")
    h1 = get_market("1h")
    h4 = get_market("4h")

    reports = [m15, h1, h4]

    avg_score = (m15["score"] + h1["score"] + h4["score"]) / 3

    if avg_score >= 75:

        final_signal = "🟢 STRONG BUY"

    elif avg_score <= 35:

        final_signal = "🔴 STRONG SELL"

    else:

        final_signal = "🟡 HOLD"

    sl, tp = risk_management(m15["price"], final_signal)

    message = f"""


💰 PRICE
{round(m15['price'],2)} USDT


📊 TIMEFRAME ANALYSIS


15M:
{m15['signal']}
AI Score: {m15['score']}%


1H:
{h1['signal']}
AI Score: {h1['score']}%


4H:
{h4['signal']}
AI Score: {h4['score']}%



🧠 FINAL SIGNAL

{final_signal}


🎯 STOP LOSS
{round(sl,2)}


🎯 TAKE PROFIT
{round(tp,2)}


"""

    print(message)

    save_trade(final_signal, m15["price"])

    if BOT_TOKEN:

        await bot.send_message(chat_id=CHAT_ID, text=message)

        print("✅ Telegram Sent")

    print("📒 Journal Updated")


if __name__ == "__main__":

    asyncio.run(main())
