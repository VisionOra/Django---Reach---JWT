from decimal import Decimal

import requests


def get_ethereum_balance(address):
    try:
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": "UZRN9A9QR78Z44JNWEFVEUSNT3EW6W5JSV",
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()
        balance = response_data.get("result")
        return Decimal(balance) / Decimal(
            "1000000000000000000"
        )  # Convert from Wei to Ether
    except (requests.RequestException, ValueError) as e:
        # Log the exception or handle it appropriately
        print(f"Error fetching Ethereum balance: {e}")
        return Decimal("0")  # Return 0 or handle as needed
