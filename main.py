import csv
import time
from fetch_data import get_wallet_transactions
from risk_scoring import compute_features, compute_score

# Read wallets from wallets.txt
with open("wallets.txt") as f:
    wallets = [line.strip() for line in f if line.strip()]

with open("wallet_scores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["wallet_id", "score"])
    for w in wallets:
        txs = get_wallet_transactions(w)
        features = compute_features(txs)
        score = compute_score(features)
        writer.writerow([w, score])
        print(f"{w} => {score}")
        time.sleep(0.2)  # to avoid API rate limit
