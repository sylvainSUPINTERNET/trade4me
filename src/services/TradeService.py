import logging
from src.coinbase.Configuration import Configuration
from dotenv import dotenv_values
import requests

logging.basicConfig(level=logging.DEBUG)

"""
Return fee to pay related on price of transaction
https://help.coinbase.com/en/pro/trading-and-funding/trading-rules-and-fees/fees
maker = waiting list in market order book
taker = direct sell
"""
async def get_fee(position, price):
    coinbase_pro_client = Configuration(dotenv_values(".env"))
    resp = requests.get(coinbase_pro_client.api_rest_base_url + 'fees', auth=coinbase_pro_client)
    if resp.status_code == 200:
        # {'maker_fee_rate': '0.0050', 'taker_fee_rate': '0.0050', 'usd_volume': None}
        data = resp.json()
        if position == "taker":
            return float(price) * float(data["taker_fee_rate"])
        if position == "maker":
            return float(price) * float(data["maker_fee_rate"])


async def buy_coin():
    logging.info(f"Buying ...")

async def sell_coin():
    logging.info(f"Selling ...")