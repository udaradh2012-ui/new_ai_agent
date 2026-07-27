# ==========================================
# BTC AI AGENT v15 CLEAN
# PROFESSIONAL STREAMLIT DASHBOARD
# PART 1 / 3
# ==========================================


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from streamlit_autorefresh import st_autorefresh

# ==========================================
# IMPORT MODULES
# ==========================================


from data_provider import get_live_price, get_24h_change, get_ohlcv


from indicators import add_indicators, analyze_signal


from risk_manager import calculate_trade_plan


from market_analysis import market_strength


from support_resistance import calculate_levels


from fibonacci import calculate_fibonacci


from ai_summary import generate_summary


from reason_engine import generate_reason


from volume_analysis import analyze_volume


from ai_engine import calculate_ai_score


from ai_decision import smart_decision


from candlestick import detect_pattern


from wallet import load_wallet


from trade_manager import open_trade, check_position, check_tp_sl, update_trailing_stop


from trade_performance import get_statistics


from performance import get_performance


from trade_mode import detect_trade_mode


from ai_quality import calculate_ai_quality


from ai_trade_journal import get_journal


from config import SYMBOL, COINS


from multi_scanner import scan_market

from pullback_filter import detect_pullback

from entry_quality import calculate_entry_quality

# ==========================================
# PAGE CONFIG
# ==========================================


st.set_page_config(page_title="BTC AI Agent v15 Clean", page_icon="🚀", layout="wide")


# ==========================================
# AUTO REFRESH
# ==========================================


st_autorefresh(interval=30000, key="btc_refresh")


# ==========================================
# TITLE
# ==========================================


st.title("🚀 BTC AI AGENT PRO v15 CLEAN")


st.caption("Professional Bitcoin Trading Intelligence Dashboard")


# ==========================================
# MARKET SCANNER
# ==========================================


@st.cache_data(ttl=30)
def get_market_scan():

    return scan_market()


market_results = get_market_scan()


best_coin = None


if market_results:

    best_coin = market_results[0]


# ==========================================
# LOAD WALLET
# ==========================================


wallet = load_wallet()


# ==========================================
# FIND ACTIVE POSITION COIN
# ==========================================


def get_active_coin(wallet):

    for coin, position in wallet["positions"].items():

        if position.get("open_position", False):

            return coin

    return None


active_coin = get_active_coin(wallet)


# ==========================================
# SELECT SYMBOL
# ==========================================


def get_selected_symbol():

    if active_coin:

        return active_coin

    if best_coin:

        return best_coin["coin"]

    return SYMBOL


selected_symbol = get_selected_symbol()


# ==========================================
# LOAD MARKET DATA
# ==========================================


@st.cache_data(ttl=30)
def load_market_data(symbol):

    price = get_live_price(symbol)

    change = get_24h_change(symbol)

    m15_df = add_indicators(get_ohlcv(symbol, "15m"))

    h1_df = add_indicators(get_ohlcv(symbol, "1h"))

    h4_df = add_indicators(get_ohlcv(symbol, "4h"))

    return (price, change, m15_df, h1_df, h4_df)


price, change, m15_df, h1_df, h4_df = load_market_data(selected_symbol)


current_price = price


# ==========================================
# PRICE HEADER
# ==========================================


c1, c2 = st.columns(2)


with c1:

    st.metric(f"💰 {selected_symbol} PRICE", f"${current_price:,.6f}")


with c2:

    st.metric("📈 24H CHANGE", f"{change:.2f}%")


# ==========================================
# BEST AI OPPORTUNITY
# ==========================================


st.divider()

st.subheader("🏆 BEST AI OPPORTUNITY")


if best_coin:

    st.success(f"🔥 AI SCANNED COIN : {best_coin['coin']}")

    a1, a2, a3, a4 = st.columns(4)

    with a1:

        st.metric("Signal", best_coin["signal"])

    with a2:

        st.metric("AI Score", f"{best_coin['score']}%")

    with a3:

        st.metric("Confidence", f"{best_coin['score']}%")

    with a4:

        st.metric("Risk", "MEDIUM")


else:

    st.warning("NO GOOD SETUP FOUND")

    # ==========================================
# ALL COIN SCAN RESULTS
# ==========================================


st.divider()

st.subheader("📊 ALL COIN SCAN RESULTS")


if market_results:

    for result in market_results[:10]:

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.write(f"🪙 {result['coin']}")

        with c2:

            st.write(result["signal"])

        with c3:

            st.write(f"AI Score : {result['score']}%")

        with c4:

            if result["score"] >= 70:

                st.success("GOOD SETUP")

            elif result["score"] >= 50:

                st.warning("WATCH")

            else:

                st.error("WEAK")


else:

    st.info("No coin scan data")

# ==========================================
# PART 2 / 3
# AI ENGINE + TRADE LOGIC
# ==========================================


# ==========================================
# SIGNAL ANALYSIS
# ==========================================


m15 = analyze_signal(m15_df)

h1 = analyze_signal(h1_df)

h4 = analyze_signal(h4_df)


# ==========================================
# CANDLE PATTERN
# ==========================================


pattern = detect_pattern(m15_df)


# ==========================================
# SUPPORT RESISTANCE
# ==========================================


levels = calculate_levels(m15_df)


# ==========================================
# FIBONACCI
# ==========================================


fib_levels = calculate_fibonacci(m15_df)


# ==========================================
# VOLUME ANALYSIS
# ==========================================


volume = analyze_volume(m15_df)


# ==========================================
# AI SCORE
# ==========================================


ai_score = calculate_ai_score(
    m15, h1, h4, volume["score"], levels["score"], fib_levels["score"], pattern["score"]
)


# ==========================================
# MARKET STRENGTH
# ==========================================


strength = market_strength([m15, h1, h4])


# ==========================================
# AI SUMMARY
# ==========================================


summary = generate_summary(m15, h1, h4, levels, fib_levels)


# ==========================================
# TIMEFRAME DISPLAY
# ==========================================


st.divider()

st.subheader("📊 AI TIMEFRAME ANALYSIS")


t1, t2, t3 = st.columns(3)


with t1:

    st.metric("15M", m15["signal"])

    st.write(f"AI Score : {m15['score']}%")


with t2:

    st.metric("1H", h1["signal"])

    st.write(f"AI Score : {h1['score']}%")


with t3:

    st.metric("4H", h4["signal"])

    st.write(f"AI Score : {h4['score']}%")


# ==========================================
# FINAL AI DECISION
# ==========================================


final_signal = smart_decision(m15, h1, h4, ai_score)


reason = generate_reason(m15, h1, h4, volume, pattern, strength, ai_score, final_signal)


trade_mode = detect_trade_mode(m15, h1, h4, ai_score)

# ==========================================
# ENTRY QUALITY SCORE
# ==========================================

pullback_signal = detect_pullback(m15_df, final_signal)

entry_quality = calculate_entry_quality(
    final_signal=final_signal,
    pullback_signal=pullback_signal,
    volume_score=volume["score"],
    atr=m15["atr"],
    price=current_price,
    support=levels["support"],
    resistance=levels["resistance"],
    ema20=m15_df["EMA20"].iloc[-1],
    ema50=m15_df["EMA50"].iloc[-1],
)


# ==========================================
# FINAL DECISION DISPLAY
# ==========================================


st.divider()

st.subheader("🧠 FINAL AI DECISION")


if "BUY" in final_signal:

    st.success(final_signal)


elif "SELL" in final_signal:

    st.error(final_signal)


else:

    st.warning(final_signal)


# ==========================================
# TRADE MODE
# ==========================================


st.divider()

st.subheader("⚡ TRADE MODE")


m1, m2, m3 = st.columns(3)


with m1:

    st.metric("Mode", trade_mode["mode"])


with m2:

    st.metric("Risk", trade_mode["risk"])


with m3:

    st.write(trade_mode["reason"])


# ==========================================
# TRADE FILTER
# ==========================================

allow_trade = True


# Entry Quality Filter

if entry_quality["score"] < 50:

    allow_trade = False

    quality_message = "🔴 ENTRY QUALITY TOO LOW"


elif entry_quality["score"] < 65:

    allow_trade = False

    quality_message = "⚠️ LOW QUALITY / WAIT"


else:

    quality_message = "✅ HIGH QUALITY ENTRY"


# AI Score Filter

if ai_score < 40:

    allow_trade = False


# Trend confirmation

if "BUY" in final_signal:

    if "BUY" not in m15["signal"] or "BUY" not in h1["signal"]:

        allow_trade = False


elif "SELL" in final_signal:

    if "SELL" not in m15["signal"] or "SELL" not in h1["signal"]:

        allow_trade = False

# ==========================================
# TRADE PLAN
# ==========================================


if trade_mode["mode"] == "📈 NORMAL TRADE":

    plan = calculate_trade_plan(price, final_signal, "NORMAL")


elif trade_mode["mode"] == "⚡ SCALPING MODE":

    plan = calculate_trade_plan(price, final_signal, "SCALP", m15["atr"])


else:

    plan = {"entry": price, "stop_loss": None, "take_profit": None, "risk_reward": None}

# ==========================================
# ENTRY QUALITY
# ==========================================

st.divider()

st.subheader("⭐ ENTRY QUALITY")

q1, q2 = st.columns(2)

with q1:
    st.metric("Entry Score", f"{entry_quality['score']}/100")

with q2:
    if entry_quality["score"] >= 80:
        st.success(entry_quality["status"])
    elif entry_quality["score"] >= 65:
        st.warning(entry_quality["status"])
    else:
        st.error(entry_quality["status"])

        st.write(
            "Pullback:",
            entry_quality["pullback"],
            "| Volume:",
            entry_quality["volume"],
            "| ATR:",
            entry_quality["atr"],
            "| S/R:",
            entry_quality["sr"],
            "| Trend:",
            entry_quality["trend"],
        )

# ==========================================
# TRADE FILTER DISPLAY
# ==========================================


st.divider()

st.subheader("🛡️ TRADE FILTER")


if allow_trade:

    st.success("✅ TRADE ALLOWED")

else:

    st.warning(quality_message)
# ==========================================
# AUTO PAPER TRADING
# ==========================================


# Reload latest wallet data
wallet = load_wallet()


has_open_trade = False


for pos in wallet["positions"].values():

    if pos.get("open_position", False):

        has_open_trade = True

        break


if (
    allow_trade
    and not has_open_trade
    and plan is not None
    and plan.get("stop_loss") is not None
    and plan.get("take_profit") is not None
):

    trade_reason = " | ".join(reason) if isinstance(reason, list) else str(reason)

    if "BUY" in final_signal:

        result = open_trade(
            selected_symbol,
            current_price,
            "BUY",
            plan["stop_loss"],
            plan["take_profit"],
            ai_score,
            ai_score,
            final_signal,
            trade_reason,
        )

    elif "SELL" in final_signal:

        result = open_trade(
            selected_symbol,
            current_price,
            "SELL",
            plan["stop_loss"],
            plan["take_profit"],
            ai_score,
            ai_score,
            final_signal,
            trade_reason,
        )

    # Reload wallet after opening trade

    wallet = load_wallet()

    selected_position = wallet["positions"].get(selected_symbol, {})


else:

    if has_open_trade:

        st.info("📌 Existing trade running")

    else:

        st.info("⏳ Waiting for setup")

# ==========================================
# TRADE PLAN DISPLAY
# ==========================================


st.divider()

st.subheader("🎯 TRADE PLAN")


p1, p2, p3, p4 = st.columns(4)


with p1:

    st.metric("Entry", f"${plan['entry']:,.6f}")


with p2:

    st.metric(
        "Stop Loss",
        ("Waiting" if plan["stop_loss"] is None else f"${plan['stop_loss']:,.6f}"),
    )


with p3:

    st.metric(
        "Take Profit",
        ("Waiting" if plan["take_profit"] is None else f"${plan['take_profit']:,.6f}"),
    )


with p4:

    st.metric(
        "Risk Reward",
        ("Waiting" if plan["risk_reward"] is None else f"1:{plan['risk_reward']}"),
    )


# ==========================================
# TRAILING STOP UPDATE
# ==========================================


update_trailing_stop(selected_symbol, current_price, m15["atr"])

# ==========================================
# PART 3 / 3
# DASHBOARD DISPLAY + CHARTS + PERFORMANCE
# ==========================================


# ==========================================
# CURRENT POSITION
# ==========================================


selected_position = wallet["positions"].get(selected_symbol, {})


if selected_position.get("open_position", False):

    position = check_position(selected_symbol, current_price)


else:

    position = {"status": "NO POSITION", "pnl": 0, "pnl_percent": 0}


# ==========================================
# TP / SL CHECK
# ==========================================

tp_result = {}

if selected_position.get("open_position", False):

    tp_result = check_tp_sl(selected_symbol, current_price)

    if tp_result.get("action") == "TP":
        st.success(f"🎯 TAKE PROFIT HIT | ${tp_result.get('profit_loss', 0)}")

    elif tp_result.get("action") == "SL":
        st.error(f"🛑 STOP LOSS HIT | ${tp_result.get('profit_loss', 0)}")

# ==========================================
# VIRTUAL WALLET
# ==========================================


st.divider()

st.subheader("💰 VIRTUAL WALLET")


w1, w2, w3, w4, w5 = st.columns(5)


with w1:

    st.metric("Balance", f"${wallet['balance']:,.2f}")


with w2:

    equity = wallet["balance"]

    if position.get("status") == "OPEN":

        equity += position.get("pnl", 0)

    st.metric("Equity", f"${equity:,.2f}")


with w3:

    st.metric("Profit", f"${wallet['profit']:,.2f}")


with w4:

    st.metric("Loss", f"${wallet['loss']:,.2f}")


with w5:

    if selected_position.get("open_position", False):

        if selected_position.get("side") == "BUY":

            st.success("🟢 BUY")

        elif selected_position.get("side") == "SELL":

            st.error("🔴 SELL")

        else:

            st.info("🟡 OPEN")

    else:

        st.metric("Position", "⚪ NONE")


# ==========================================
# LIVE PNL
# ==========================================


if position.get("status") == "OPEN":

    st.divider()

    st.subheader(f"📈 LIVE PNL - {selected_symbol}")

    p1, p2, p3, p4, p5 = st.columns(5)

    with p1:

        st.metric("Entry Price", f"${position.get('entry',0):,.6f}")

    with p2:

        st.metric("Profit/Loss", f"${position.get('pnl',0):.2f}")

    with p3:

        st.metric("Current Price", f"${position.get('current',0):,.6f}")

    with p4:

        st.metric("PnL %", f"{position.get('pnl_percent',0):.2f}%")

    with p5:

        tp = position.get("take_profit")

        if tp:

            st.metric("🎯 TP", f"${tp:,.6f}")

        else:

            st.metric("🎯 TP", "N/A")

    with p5:

        sl = position.get("stop_loss")

        if sl:

            st.metric("🛑 SL", f"${sl:,.6f}")

        else:

            st.metric("🛑 SL", "N/A")


else:

    st.info(f"🟡 No Open Position - {selected_symbol}")

# ==========================================
# TRADE STATUS
# ==========================================


st.divider()

st.subheader("📊 TRADE STATUS")


if position.get("status") == "OPEN":

    entry = position.get("entry")

    tp = position.get("take_profit")

    sl = position.get("stop_loss")

    current = position.get("current")

    if position.get("side") == "BUY":

        tp_distance = tp - current if tp else 0

        sl_distance = current - sl if sl else 0

    else:

        tp_distance = current - tp if tp else 0

        sl_distance = sl - current if sl else 0

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric("🎯 TP Distance", f"${tp_distance:,.6f}")

    with s2:

        st.metric("🛑 SL Distance", f"${sl_distance:,.6f}")

    with s3:

        st.metric("Status", "RUNNING")


else:

    st.info("No open position")


# ==========================================
# SUPPORT RESISTANCE
# ==========================================


st.divider()

st.subheader("📌 SUPPORT & RESISTANCE")


s1, s2 = st.columns(2)


with s1:

    st.metric("Support", f"${levels['support']:,.2f}")


with s2:

    st.metric("Resistance", f"${levels['resistance']:,.2f}")


# ==========================================
# FIBONACCI
# ==========================================


st.divider()

st.subheader("📐 FIBONACCI LEVELS")


for level, value in fib_levels.items():

    st.write(f"{level} : ${value:,.2f}")


# ==========================================
# LIVE CANDLE CHART
# ==========================================


st.divider()

st.subheader(f"📈 {selected_symbol} CHART")


fig = go.Figure()


fig.add_trace(
    go.Candlestick(
        x=m15_df["time"],
        open=m15_df["open"],
        high=m15_df["high"],
        low=m15_df["low"],
        close=m15_df["close"],
    )
)


fig.add_trace(go.Scatter(x=m15_df["time"], y=m15_df["EMA20"], name="EMA20"))


fig.add_trace(go.Scatter(x=m15_df["time"], y=m15_df["EMA50"], name="EMA50"))


fig.update_layout(height=600, xaxis_rangeslider_visible=False)


st.plotly_chart(fig, use_container_width=True)


# ==========================================
# VOLUME
# ==========================================


st.divider()

st.subheader("📊 VOLUME ANALYSIS")


st.write(volume)


# ==========================================
# AI REASON
# ==========================================


st.divider()

st.subheader("🧠 AI REASON")


if isinstance(reason, list):

    for r in reason:

        st.write(r)

else:

    st.write(reason)


# ==========================================
# AI SUMMARY
# ==========================================


st.divider()

st.subheader("📝 AI SUMMARY")


st.markdown(summary)


# ==========================================
# PERFORMANCE
# ==========================================


st.divider()

st.subheader("🏆 PERFORMANCE")


stats = get_statistics()


p1, p2, p3, p4, p5 = st.columns(5)


with p1:

    st.metric("Trades", stats["trades"])


with p2:

    st.metric("Wins", stats["wins"])


with p3:

    st.metric("Losses", stats["losses"])


with p4:

    st.metric("Win Rate", f"{stats['win_rate']}%")


with p5:

    st.metric("Profit", f"${stats['profit']:.2f}")


# ==========================================
# TRADING HISTORY
# ==========================================

st.divider()

st.subheader("📒 TRADING HISTORY")


try:

    history = pd.read_csv("trading_history.csv")

    if len(history) > 0:

        # Latest trade first
        history = history.iloc[::-1]

        def color_side(value):

            if value == "BUY":
                return "🟢 BUY"

            elif value == "SELL":
                return "🔴 SELL"

            return value

        history["Side"] = history["Side"].apply(color_side)

        st.dataframe(history, use_container_width=True, hide_index=True)

        # Summary

        total_history = len(history)

        st.caption(f"Total Closed Trades: {total_history}")

    else:

        st.info("No history yet")


except FileNotFoundError:

    st.info("No history yet")

# ==========================================
# AI JOURNAL
# ==========================================


st.divider()

st.subheader("📖 AI TRADE JOURNAL")


journal = get_journal()


if journal:

    for trade in reversed(journal[-10:]):

        st.write(f"""
Date: {trade['date']}

Coin: {trade['coin']}

Side: {trade['side']}

PnL: ${trade['pnl']}

AI Score: {trade['ai_score']}

Confidence: {trade['confidence']}%

Trend: {trade['trend']}

Reason:
{trade['reason']}

---------------------
""")


else:

    st.info("No AI trades recorded")
