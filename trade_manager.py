# ==========================================
# BTC AI AGENT PRO v15
# PAPER TRADE MANAGER
# ==========================================

from datetime import datetime
from wallet import load_wallet, save_wallet
from trade_performance import update_performance
from ai_trade_journal import add_trade_journal
from history_manager import save_trade


def open_trade(
    coin,
    price,
    side,
    stop_loss,
    take_profit,
    ai_score=0,
    confidence=0,
    trend="UNKNOWN",
    reason="No reason",
):

    wallet = load_wallet()

    position = wallet["positions"][coin]

    if position["open_position"]:

        return {"status": "Position already open"}

    quantity = wallet["balance"] / price

    position["open_position"] = True

    position["side"] = side

    position["entry_price"] = price

    position["quantity"] = round(quantity, 6)

    position["stop_loss"] = stop_loss

    position["take_profit"] = take_profit

    position["trade_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    position["ai_score"] = ai_score

    position["confidence"] = confidence

    position["trend"] = trend

    position["reason"] = reason

    save_wallet(wallet)

    return {
        "status": "Trade opened",
        "coin": coin,
        "side": side,
        "price": price,
        "quantity": position["quantity"],
    }


# ==========================================
# CHECK POSITION
# ==========================================

from wallet import load_wallet, save_wallet

# ==========================================
# CHECK POSITION (MULTI COIN)
# ==========================================


def check_position(coin, current_price):

    wallet = load_wallet()

    position = wallet["positions"][coin]

    if not position["open_position"]:

        return {"status": "No open position"}

    entry = position["entry_price"]

    quantity = position["quantity"]

    side = position["side"]

    if side == "BUY":

        pnl = (current_price - entry) * quantity

    elif side == "SELL":

        pnl = (entry - current_price) * quantity

    else:

        pnl = 0

    pnl_percent = (pnl / wallet["balance"]) * 100

    return {
        "status": "OPEN",
        "coin": coin,
        "side": side,
        "entry": entry,
        "current": current_price,
        "quantity": quantity,
        "take_profit": position["take_profit"],
        "stop_loss": position["stop_loss"],
        "pnl": round(pnl, 2),
        "pnl_percent": round(pnl_percent, 2),
    }


# ==========================================
# CLOSE TRADE (MULTI COIN)
# ==========================================


def close_trade(coin, current_price):

    wallet = load_wallet()

    position = wallet["positions"][coin]

    if not position.get("open_position", False):

        return {"status": "No trade"}

    result = check_position(coin, current_price)

    pnl = result["pnl"]

    update_performance(
        side=position["side"],
        entry=position["entry_price"],
        exit_price=current_price,
        pnl=pnl,
    )

    add_trade_journal(
        coin=coin,
        side=position["side"],
        entry=position["entry_price"],
        exit_price=current_price,
        pnl=pnl,
        ai_score=position.get("ai_score", 0),
        confidence=position.get("confidence", 0),
        trend=position.get("trend", "UNKNOWN"),
        reason=position.get("reason", "Trade closed"),
    )

    save_trade(
        coin=coin,
        side=position["side"],
        entry=position["entry_price"],
        exit_price=current_price,
        pnl=pnl,
        ai_score=position.get("ai_score", 0),
        confidence=position.get("confidence", 0),
        reason=position.get("reason", "Trade closed"),
    )

    wallet["balance"] += pnl

    if pnl >= 0:
        wallet["profit"] += pnl
    else:
        wallet["loss"] += abs(pnl)

    wallet["equity"] = wallet["balance"]

    # reset position

    position["open_position"] = False
    position["side"] = ""
    position["entry_price"] = 0
    position["quantity"] = 0
    position["stop_loss"] = 0
    position["take_profit"] = 0

    save_wallet(wallet)

    return {"status": "Closed", "profit_loss": round(pnl, 2)}


# ==========================================
# CHECK TP / SL (MULTI COIN)
# ==========================================


def check_tp_sl(coin, current_price):

    wallet = load_wallet()

    position = wallet["positions"][coin]

    if not position.get("open_position", False):

        return {"status": "No position"}

    side = position["side"]

    tp = position["take_profit"]

    sl = position["stop_loss"]

    if side == "BUY":

        if current_price >= tp:

            result = close_trade(coin, current_price)

            result["action"] = "TP"

            return result

        elif current_price <= sl:

            result = close_trade(coin, current_price)

            result["action"] = "SL"

            return result

    elif side == "SELL":

        if current_price <= tp:

            result = close_trade(coin, current_price)

            result["action"] = "TP"

            return result

        elif current_price >= sl:

            result = close_trade(coin, current_price)

            result["action"] = "SL"

            return result

    return {"status": "OPEN", "action": "HOLD", "price": current_price}


# ==========================================
# TRAILING STOP LOSS (MULTI COIN)
# ==========================================


def update_trailing_stop(coin, current_price, atr):

    wallet = load_wallet()

    position = wallet["positions"].get(coin, {})

    if not position.get("open_position", False):

        return {"status": "No position"}

    side = position.get("side", "")

    entry = position.get("entry_price", 0)

    old_sl = position.get("stop_loss", 0)

    trailing_atr = atr * 0.5

    # ==========================
    # BUY TRAILING STOP
    # ==========================

    if side == "BUY":

        new_sl = current_price - trailing_atr

        if new_sl > old_sl and new_sl > entry:

            position["stop_loss"] = round(new_sl, 2)

            save_wallet(wallet)

            return {
                "status": "SL UPDATED",
                "coin": coin,
                "old_sl": old_sl,
                "new_sl": position["stop_loss"],
            }

    # ==========================
    # SELL TRAILING STOP
    # ==========================

    elif side == "SELL":

        new_sl = current_price + trailing_atr

        if new_sl < old_sl and new_sl < entry:

            position["stop_loss"] = round(new_sl, 2)

            save_wallet(wallet)

            return {
                "status": "SL UPDATED",
                "coin": coin,
                "old_sl": old_sl,
                "new_sl": position["stop_loss"],
            }

    return {"status": "NO CHANGE", "coin": coin}
