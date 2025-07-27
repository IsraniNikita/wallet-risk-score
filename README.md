# Wallet Risk Scoring – Compound Protocol

- This project calculates risk scores (0–1000) for a list of Ethereum wallet addresses based on their interaction with the **Compound V2 protocol**.  
- The final deliverable is a CSV file containing each wallet's risk score.

---

## **Project Structure**
```
fetch_data.py # Fetches transaction data from Etherscan

risk_scoring.py # Creates features & computes scores

main.py # Orchestrates data fetching & scoring

wallets.txt # List of wallet addresses

wallet_scores.csv # Final output with scores
```

---

## **Data Collection Method**

- We used the **Etherscan API** to fetch on-chain transaction history for each wallet.  
- We filtered transactions to only include interactions with **Compound V2 contracts**:  
  - `0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643` - cDAI  
  - `0x4ddc2D193948926d02f9B1fE9e1daa0718270ED5` - cETH  
  - `0x39AA39c021dfbaE8faC545936693aC917d5E7563` - cUSDC  
  - `0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643` - cDAI
  - `0x4ddc2D193948926d02f9B1fE9e1daa0718270ED5` - cETH
  - `0x39AA39c021dfbaE8faC545936693aC917d5E7563` - cUSDC
  - `0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9` - cUSDT
  - `0xccF4429DB6322D5C611ee964527D42E5d685DD6a` -  cWBTC
  - `0x35A18000230DA775CAc24873d00Ff85BccdeD550` -  cUNI
  - `0xFAce851a4921ce59e912d19329929CE6da6EB0c7` -  cLINK
  - `0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E` -  cBAT
  -  `0xB3319f5D18Bc0D84dD1b4825Dcde5d5f7266d407` -  cZRX
  - `0x80a2AE356fc9ef4305676f7a3E2ED04e12C33946` -  cREP (old market)

Example Etherscan API call:
```
?module=account
&action=txlist
&address=<wallet_address>
&startblock=0
&endblock=99999999
&sort=asc
&apikey=<YOUR_API_KEY>
```

---

## **Feature Selection Rationale**

For each wallet, we created the following features:

- **total_txs** – Number of Compound protocol transactions.  
  *Why?* A wallet with more activity is considered more trusted and less risky.  

- **total_value** – Total ETH value (in Wei) transacted with Compound.  
  *Why?* Larger value transfers suggest stronger engagement with the protocol.  

- **avg_value** – Average transaction value.  
  *Why?* Consistently high-value transactions indicate less likelihood of spam or dusting attacks.

---

## **Scoring Method**

We used a **0–1000 risk score** based on the following formula:

```python
score = 0
score += min(features["total_txs"] * 10, 400)       # Up to 400 points
score += min(features["total_value"] / 1e18, 500)   # Up to 500 points (ETH)
score += min(features["avg_value"] / 1e18, 100)     # Up to 100 points
return int(min(score, 1000))                        # Cap at 1000
```
Why this scale?

- Active wallets (many transactions) are rewarded.

- High total & average value transactions increase trust.

- Final score is capped at 1000 for normalization.

---

## **Risk Indicators Justification**
- Low score (0–200): Wallets with minimal or no interaction with Compound (high risk).

- Medium score (200–600): Wallets with moderate transactions or low value.

- High score (600–1000): Active, high-value wallets (low risk).

---

## **Deliverables**
- CSV File:
Format:
```
wallet_id,score
0xfaa0768bde629806739c3a4620656c5d26f44ef2,732
```
Example (from our output):
```
wallet_id,score
0x0039f22efb07a647557c7c5d17854cfd6d489ef3,438
0x06b51c6882b27cb05e712185531c1f74996dd988,10
...
```
- Code Files:
```
fetch_data.py

risk_scoring.py

main.py

wallets.txt
```

- Analysis & Insights

For a detailed analysis of the wallet scores, distribution charts, and behavioral insights across score ranges, refer to:  
[**analysis.md**](analysis.md)

---

## **How to Run**
1. Install dependencies:
```
pip install requests
```
2. Add your Etherscan API key to fetch_data.py.
3. Run the pipeline:
```
python main.py

```
4. Final results will be in:
```
wallet_scores.csv

```

--- 

## **Scalability**
- The solution can handle any number of wallets (rate-limited by Etherscan API).

- The scoring logic is modular and can easily include more features (e.g., borrow/repay patterns).

- This approach can be extended to other lending protocols by adding contract addresses.




