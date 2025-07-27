def compute_features(transactions):
    """
    Create simple features for risk scoring.
    """
    total_txs = len(transactions)
    total_value = sum(int(tx["value"]) for tx in transactions)  # in Wei
    avg_value = total_value / total_txs if total_txs > 0 else 0

    return {
        "total_txs": total_txs,
        "total_value": total_value,
        "avg_value": avg_value
    }

def compute_score(features):
    """
    A simple scoring logic:
    - More transactions and value = lower risk (higher score)
    """
    score = 0
    score += min(features["total_txs"] * 10, 400)  # up to 400 points
    score += min(features["total_value"] / 1e18, 500)  # up to 500 points (ETH)
    score += min(features["avg_value"] / 1e18, 100)   # up to 100 points
    return int(min(score, 1000))  # max 1000
