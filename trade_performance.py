import json
import os
from datetime import datetime

PERFORMANCE_FILE = "performance.json"


DEFAULT_DATA = {
    "balance": 500.0,
    "starting_balance": 500.0,
    "total_profit": 0.0,
    "total_trades": 0,
    "wins": 0,
    "losses": 0,
    "best_trade": 0.0,
    "worst_trade": 0.0,
    "equity_curve": [500.0],
    "history": [],
}


# ==========================================
# LOAD PERFORMANCE
# ==========================================


def load_performance():

    if not os.path.exists(PERFORMANCE_FILE):

        save_performance(DEFAULT_DATA)

        return DEFAULT_DATA.copy()

    with open(PERFORMANCE_FILE, "r") as f:

        return json.load(f)


# ==========================================
# SAVE PERFORMANCE
# ==========================================


def save_performance(data):

    with open(PERFORMANCE_FILE, "w") as f:

        json.dump(data, f, indent=4)


# ==========================================
# UPDATE PERFORMANCE AFTER TRADE CLOSE
# ==========================================


def update_performance(side, entry, exit_price, pnl):

    data = load_performance()

    data["total_profit"] += pnl

    data["balance"] += pnl

    data["total_trades"] += 1

    if pnl > 0:

        data["wins"] += 1

    else:

        data["losses"] += 1

    if pnl > data["best_trade"]:

        data["best_trade"] = pnl

    if pnl < data["worst_trade"]:

        data["worst_trade"] = pnl

    data["equity_curve"].append(data["balance"])

    trade = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "side": side,
        "entry": entry,
        "exit": exit_price,
        "pnl": round(pnl, 2),
        "result": "WIN" if pnl > 0 else "LOSS",
    }

    data["history"].append(trade)

    save_performance(data)


# ==========================================
# STATISTICS
# ==========================================


def get_statistics():

    data = load_performance()

    if data["total_trades"] > 0:

        win_rate = (data["wins"] / data["total_trades"]) * 100

    else:

        win_rate = 0

    winning_trades = [t["pnl"] for t in data["history"] if t["pnl"] > 0]

    losing_trades = [t["pnl"] for t in data["history"] if t["pnl"] < 0]

    average_win = sum(winning_trades) / len(winning_trades) if winning_trades else 0

    average_loss = sum(losing_trades) / len(losing_trades) if losing_trades else 0

    total_win = sum(winning_trades)

    total_loss = abs(sum(losing_trades))

    # =================================
    # PROFIT FACTOR
    # =================================

    if total_loss > 0:

        profit_factor = total_win / total_loss

    else:

        profit_factor = float("inf")

    # =================================
    # DRAWDOWN
    # =================================

    equity = data["equity_curve"]

    peak = equity[0]

    max_drawdown = 0

    for value in equity:

        if value > peak:

            peak = value

        drawdown = ((peak - value) / peak) * 100

        if drawdown > max_drawdown:

            max_drawdown = drawdown

    return {
        "balance": data["balance"],
        "profit": data["total_profit"],
        "trades": data["total_trades"],
        "wins": data["wins"],
        "losses": data["losses"],
        "win_rate": round(win_rate, 2),
        "best_trade": data["best_trade"],
        "worst_trade": data["worst_trade"],
        "average_win": round(average_win, 2),
        "average_loss": round(average_loss, 2),
        "profit_factor": profit_factor,
        "max_drawdown": round(max_drawdown, 2),
        "equity_curve": data["equity_curve"],
        "history": data["history"],
    }


# ==========================================
# RESET
# ==========================================


def reset_performance():

    save_performance(DEFAULT_DATA.copy())
