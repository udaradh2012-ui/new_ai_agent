# ==========================================
# BTC AI AGENT v18 PRO
# DYNAMIC RISK MANAGER
# ==========================================

from config import RISK_REWARD, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT


def calculate_trade_plan(
    price, signal, mode="NORMAL", atr=0, support=None, resistance=None
):

    # ==========================================
    # NO SIGNAL
    # ==========================================

    if "BUY" not in signal and "SELL" not in signal:

        return {
            "direction": "NO TRADE",
            "entry": price,
            "stop_loss": None,
            "take_profit": None,
            "risk_reward": RISK_REWARD,
        }

    # ==========================================
    # SCALPING MODE
    # ==========================================

    if mode == "SCALP":

        # ATR fallback
        if atr is None or atr <= 0:
            sl_distance = price * 0.003
            tp_distance = price * 0.006
        else:
            sl_distance = atr * 2.0
            tp_distance = atr * 3.0

    # ==========================================
    # NORMAL MODE
    # ==========================================

    else:

        sl_distance = price * (STOP_LOSS_PERCENT / 100)
        tp_distance = price * (TAKE_PROFIT_PERCENT / 100)

    # ==========================================
    # BUY
    # ==========================================

    if "BUY" in signal:

        stop_loss = price - sl_distance

        if support is not None:
            stop_loss = min(stop_loss, support)

        take_profit = price + tp_distance
        direction = "LONG"

    # ==========================================
    # SELL
    # ==========================================

    else:

        stop_loss = price + sl_distance

        if resistance is not None:
            stop_loss = max(stop_loss, resistance)

        take_profit = price - tp_distance
        direction = "SHORT"

    # ==========================================
    # RETURN
    # ==========================================

    return {
        "direction": direction,
        "entry": float(price),
        "stop_loss": float(stop_loss),
        "take_profit": float(take_profit),
        "risk_reward": RISK_REWARD,
    }
