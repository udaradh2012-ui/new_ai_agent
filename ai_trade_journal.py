import json
import os
from datetime import datetime

JOURNAL_FILE = "trade_journal.json"


def load_journal():

    if not os.path.exists(JOURNAL_FILE):

        return []

    with open(JOURNAL_FILE, "r") as f:

        return json.load(f)


def save_journal(data):

    with open(JOURNAL_FILE, "w") as f:

        json.dump(data, f, indent=4)


def add_trade_journal(
    coin, side, entry, exit_price, pnl, ai_score, confidence, trend, reason
):

    journal = load_journal()

    trade = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "coin": coin,
        "side": side,
        "entry": entry,
        "exit": exit_price,
        "pnl": round(pnl, 2),
        "ai_score": ai_score,
        "confidence": confidence,
        "trend": trend,
        "reason": reason,
        "result": "WIN" if pnl > 0 else "LOSS",
    }

    journal.append(trade)

    save_journal(journal)


def get_journal():

    return load_journal()
