import requests
from pprint import pprint
from src.db.Configuration import Configuration as dbConfiguration
from dotenv import dotenv_values
from aiohttp import ClientSession as session
import json
import logging

logging.basicConfig(level=logging.DEBUG)



"""

Generate product ids for WS coinbasepro ( e.g EUR-MANA not working, but MANA-EUR ok)

"""
async def get_focus_coins_id():
    db = dbConfiguration(dotenv_values(".env"))
    return [f"{i['coinTarget']}-{i['coinUse']}" for i in db.get_collection("focus").find()]


async def get_focus_details():
    db = dbConfiguration(dotenv_values(".env"))
    return list(db.get_collection("focus").find())

""" 

Using asset_name as "main" source for transaction

"""
async def allocate_budget(coinbase_pro_client, asset_name):
    logging.debug("------ API CALL ------ ")

    db = dbConfiguration(dotenv_values(".env"))

    resp = requests.get(coinbase_pro_client.api_rest_base_url + 'accounts', auth=coinbase_pro_client)
    if resp.status_code == 200:
        target_asset = list(filter(lambda x: (x["currency"] == asset_name), resp.json()))
        focus = [i for i in db.get_collection("focus").find()]
        for target in target_asset:
            logging.info(f" ------------------------------------------------------------------------------")
            logging.info(f" > Account state coinbasepro currency: {target['currency']}")
            logging.info(f" > Account state coinbasepro balance: {target['available']}")
            logging.info(f" >> Account state coinbasepro balance: {target['balance']}")
            logging.info(f" >> Account state coinbasepro hold: {target['hold']}")
            logging.info(f" >> Account state coinbasepro trading enabled: {target['trading_enabled']}")
            logging.info(f" ------------------------------------------------------------------------------")
            for coin in focus:
                if coin["coinUse"] == target["currency"]:
                    logging.info("match found in focus -> " + coin["coinUse"] + " for invest : " + coin["coinTarget"])

        # TODO => return better data
        # TODO => check what is return from API here 
        # THEN in app they are 2 steps : 
        # ============> INIT account / focus data ( itteration 0 )
        # ============> each time we call API, reset this data
        # This data will be use into dispatch => add_price => analyzis ( and in analysis we need to add the logic about budget / fee => itneressting to pay or sell ? based on df )
        return resp.json()

    else:
        print("error")



async def dispatch(wsPayload, memMarket, cleanup_signal, current_account_info, info_focus):
        data = json.loads(wsPayload)
        if "type" in data:
            if "product_id" in data:
                await memMarket.add_price(data["product_id"], data["best_bid"], data["best_ask"], cleanup_signal, current_account_info, info_focus, wsPayload)

            
    # try:
    #     data = json.loads(wsPayload)
    #     if "type" in data:
    #         if data["type"] == "ticker":
    #             if "product_id" in data:
    #                 #logging.debug(f"TICKER -> {data}")
    #                 print("================================")
    #                 print("================================")
    #                 print("================================")
    #                 print("================================")
    #                 print("================================")
    #                 print("================================")

    #                 print(json.loads(wsPayload).keys())

    #                 print("================================")
    #                 print("================================")
    #                 print("================================")
    #                 print("================================")
    #                 print("================================")
    #                 memMarket.add_price(data.product_id, data.best_bid, data.best_ask, cleanup_signal)
    #         if data["type"] == "error":
    #             logging.info(f"ERROR -> {data}")
    #         if data["type"] == "subscription":
    #             logging.info(f"SUBSCRIPTION -> {data}")
    # except Exception as e:
    #     logging.info(e)


# {'available': '100600',
#  'balance': '100600.0000000000000000',
#  'currency': 'EUR',
#  'hold': '0.0000000000000000',
#  'id': '6ef3d353-cc92-4c6a-9fff-7684e08ed499',
#  'profile_id': '3045f879-1957-4ec0-9eb8-819622d89e63',
#  'trading_enabled': True}