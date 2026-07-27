# ==========================================
# MULTI COIN WALLET MANAGER v2
# ==========================================

import json
import os

WALLET_FILE = "wallet.json"


COINS = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "SOL/USDT",
    "XRP/USDT",
    "ADA/USDT",
    "DOGE/USDT",
]


def create_position():

    return {
        "open_position": False,
        "side": "",
        "entry_price": 0,
        "quantity": 0,
        "stop_loss": 0,
        "take_profit": 0,
        "ai_score": 0,
        "confidence": 0,
        "trend": "",
        "reason": "",
        "trade_time": "",
    }


DEFAULT_WALLET = {
    "balance": 500.0,
    "equity": 500.0,
    "profit": 0.0,
    "loss": 0.0,
    "positions": {coin: create_position() for coin in COINS},
}


def load_wallet():

    if not os.path.exists(WALLET_FILE):

        save_wallet(DEFAULT_WALLET)

        return DEFAULT_WALLET.copy()

    with open(WALLET_FILE, "r") as f:

        return json.load(f)


def save_wallet(wallet):

    with open(WALLET_FILE, "w") as f:

        json.dump(wallet, f, indent=4)


def reset_wallet():

    save_wallet(DEFAULT_WALLET.copy())
