# ==========================================
# AI COIN SELECTOR v1
# ==========================================


def select_best_coin(scan_results):

    if not scan_results:

        return {"status": "NO DATA"}

    # Sort already done by scanner
    best = scan_results[0]

    # ==============================
    # FILTER
    # ==============================

    if best["score"] < 60:

        return {"status": "NO GOOD SETUP", "coin": best["coin"], "score": best["score"]}

    if best["risk"] == "HIGH":

        return {"status": "HIGH RISK", "coin": best["coin"], "score": best["score"]}

    # ==============================
    # FINAL SELECTION
    # ==============================

    return {
        "status": "SELECTED",
        "coin": best["coin"],
        "signal": best["signal"],
        "score": best["score"],
        "confidence": best["confidence"],
        "trend": best["trend"],
        "risk": best["risk"],
    }
