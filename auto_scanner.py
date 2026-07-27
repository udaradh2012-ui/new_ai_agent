import streamlit as st
import ccxt
import pandas as pd
import ta

exchange = ccxt.binance()


st.set_page_config(page_title="BTC AI Dashboard", layout="wide")


st.title("🚀 BTC AI TRADING DASHBOARD")


def analyze(timeframe):

    candles = exchange.fetch_ohlcv("BTC/USDT", timeframe=timeframe, limit=100)

    df = pd.DataFrame(
        candles, columns=["time", "open", "high", "low", "close", "volume"]
    )

    df["EMA20"] = ta.trend.EMAIndicator(df["close"], 20).ema_indicator()

    df["EMA50"] = ta.trend.EMAIndicator(df["close"], 50).ema_indicator()

    df["RSI"] = ta.momentum.RSIIndicator(df["close"], 14).rsi()

    last = df.iloc[-1]

    if last["EMA20"] > last["EMA50"]:
        trend = "BULLISH"
    else:
        trend = "BEARISH"

    if trend == "BULLISH":
        signal = "🟢 BUY"
    else:
        signal = "🔴 SELL"

    confidence = 75

    return {
        "price": last["close"],
        "trend": trend,
        "rsi": last["RSI"],
        "signal": signal,
        "confidence": confidence,
    }


m15 = analyze("15m")
h1 = analyze("1h")
h4 = analyze("4h")


col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("⚡ 15M")

    st.metric("Price", round(m15["price"], 2))

    st.write("Trend:", m15["trend"])

    st.write("Signal:", m15["signal"])


with col2:

    st.subheader("🕐 1H")

    st.metric("Price", round(h1["price"], 2))

    st.write("Trend:", h1["trend"])

    st.write("Signal:", h1["signal"])


with col3:

    st.subheader("📈 4H")

    st.metric("Price", round(h4["price"], 2))

    st.write("Trend:", h4["trend"])

    st.write("Signal:", h4["signal"])


st.divider()


st.subheader("🧠 AI FINAL DECISION")


if m15["trend"] == "BULLISH" and h4["trend"] == "BULLISH":

    st.success("🟢 BUY BIAS")

else:

    st.warning("🟡 WAIT")
