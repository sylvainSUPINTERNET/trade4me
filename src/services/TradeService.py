import logging
from src.coinbase.Configuration import Configuration
from dotenv import dotenv_values
import requests
import json
from ast import literal_eval

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


async def buy():
    # TODO compute fee to know if it's itneressting
    logging.info(f"Buying ...")


async def sell():
    # TODO compute fee to know if it's itneressting
    logging.info(f"Selling ...")
    


"""
    ((highVal - currentValue) / highVal) * 100 
"""
async def choose_action(df, globalWsResp, product_id, info_focus) -> str:
    globalWsResp = json.loads(globalWsResp)

    coinTargetList = list(filter(lambda x: x != "EUR", product_id.split("-")))
    focus = list(filter(lambda x: x["coinTarget"] == coinTargetList[0], info_focus))[0]

    logging.info(f"Chosing action for {product_id}")
    miniThresholdVariationToBuyInPercent = focus["thresholdVariationToBuyInPercent"]
    miniThresholdVariationToSellInPercent = focus["thresholdVariationToSellInPercent"]

    low_24h = globalWsResp["low_24h"]
    high_24h = globalWsResp["high_24h"]


    current_buy_price = df.iloc[len(df) - 1][f"{product_id}@buy"]
    current_sell_price = df.iloc[len(df) - 1][f"{product_id}@sell"]
    

    buy_variation = ( (float(current_buy_price) - float(low_24h)) / float(low_24h) )  * 100
    if float(buy_variation) > float(miniThresholdVariationToBuyInPercent):
        logging.info(f"Buy {product_id}, variation {buy_variation}% => mini expected : {miniThresholdVariationToBuyInPercent}% -> OK")
        return "BUY"

    sell_variation = ( (float(current_sell_price) - float(low_24h)) / float(low_24h)) * 100
    if float(sell_variation) >= float(miniThresholdVariationToSellInPercent):
        logging.info(f"Selling {product_id}, variation {sell_variation}% => mini expected : {miniThresholdVariationToSellInPercent}% -> OK")
        return "SELL"
        
    logging.info(f"No action decided for {product_id}. No interessting variation found, based on your threshold set")
    return None


async def analyze_plz(df, product_id, current_account_info, info_focus, globalWsResp):
    action = await choose_action(df, globalWsResp, product_id, info_focus)
    if action != None:
        if action == "BUY":
            await buy()
        if action == "SELL":
            await sell()

    # print("=========================================")
    # print("=========================================")
    # print("=========================================")

    # logging.info(f"Analysis request for {product_id}")
    # print("=========================================")
    
    # # {"type":"ticker","sequence":9209893819,
    # # "product_id":"ETH-EUR",
    # # "price":"3650.73","open_24h":"3691.72",
    # # "volume_24h":"32087.11762915",
    # # "low_24h":"3239.01",
    # # "high_24h":"3715",
    # # "volume_30d":"382199.72424840",
    # # "best_bid":"3649.72","best_ask":"3650.73",
    # # "side":"buy",
    # # "time":"2021-12-05T00:31:20.062761Z",
    # # "trade_id":31129727,
    # # "last_size":"0.00101627"}
    # print(current_account_info)
    # print(info_focus)
    # print(globalWsResp)

    # #await compute_variation_in_percent_to_buy(globalWsResp["high_24h"],globalWsResp["low_24h"],)
