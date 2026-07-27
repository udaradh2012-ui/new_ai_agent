import pandas as pd
from pathlib import Path
from datetime import datetime

FILE_NAME = "trading_history.csv"


COLUMNS = [
    "Time",
    "Coin",
    "Side",
    "Entry",
    "Exit",
    "PnL",
    "AI Score",
    "Confidence",
    "Reason",
]


def save_trade(coin, side, entry, exit_price, pnl, ai_score=0, confidence=0, reason=""):

    row = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Coin": coin,
        "Side": side,
        "Entry": round(entry, 2),
        "Exit": round(exit_price, 2),
        "PnL": round(pnl, 2),
        "AI Score": ai_score,
        "Confidence": confidence,
        "Reason": reason,
    }

    if Path(FILE_NAME).exists():

        df = pd.read_csv(FILE_NAME)

    else:

        df = pd.DataFrame(columns=COLUMNS)

    df.loc[len(df)] = row

    df.to_csv(FILE_NAME, index=False)
