# ==============================
# BTC AI v14
# PERFORMANCE ANALYSIS
# ==============================

import pandas as pd
from pathlib import Path

FILE_NAME = "trading_history.csv"


def get_performance():

    if not Path(FILE_NAME).exists():

        return {"total": 0, "buy": 0, "sell": 0, "hold": 0, "average_score": 0}

    df = pd.read_csv(FILE_NAME)

    total = len(df)

    buy = df[df["Signal"].str.contains("BUY", na=False)].shape[0]

    sell = df[df["Signal"].str.contains("SELL", na=False)].shape[0]

    hold = df[df["Signal"].str.contains("HOLD", na=False)].shape[0]

    average_score = round(df["AI Score"].mean(), 2)

    return {
        "total": total,
        "buy": buy,
        "sell": sell,
        "hold": hold,
        "average_score": average_score,
    }
