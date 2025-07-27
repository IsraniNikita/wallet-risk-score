import requests

ETHERSCAN_API_KEY = "YOUR_API_KEY_HERE"
ETHERSCAN_URL = "https://api.etherscan.io/api"

# Full list of Compound V2 contract addresses
COMPOUND_CONTRACTS = [
    "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643",  # cDAI
    "0x4ddc2D193948926d02f9B1fE9e1daa0718270ED5",  # cETH
    "0x39AA39c021dfbaE8faC545936693aC917d5E7563",  # cUSDC
    "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9",  # cUSDT
    "0xccF4429DB6322D5C611ee964527D42E5d685DD6a",  # cWBTC
    "0x35A18000230DA775CAc24873d00Ff85BccdeD550",  # cUNI
    "0xFAce851a4921ce59e912d19329929CE6da6EB0c7",  # cLINK
    "0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E",  # cBAT
    "0xB3319f5D18Bc0D84dD1b4825Dcde5d5f7266d407",  # cZRX
    "0x80a2AE356fc9ef4305676f7a3E2ED04e12C33946"   # cREP (old market)
]

def get_wallet_transactions(wallet):
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    data = response.json()
    if data["status"] == "1":
        txs = data["result"]
        # Filter for only Compound protocol interactions
        compound_txs = [
            tx for tx in txs if tx["to"].lower() in [c.lower() for c in COMPOUND_CONTRACTS]
        ]
        return compound_txs
    else:
        return []
