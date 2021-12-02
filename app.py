from requests.auth import AuthBase
from dotenv import dotenv_values
from src.api.CoinMiddleware import add_focus_coin
from src.coinbase.Configuration import Configuration
from src.db.Configuration import Configuration as dbConfiguration
from src.services.FundService import allocate_budget, get_focus_coins_id, dispatch
from aiohttp import web
import aiohttp_cors
import asyncio
import websockets
import json

from src.services.MemMarketFollow import MemMarketFollow

CoinbaseConfiguration = Configuration(dotenv_values(".env"))
DbConfiguration = dbConfiguration(dotenv_values(".env"))
extraConf = dotenv_values(".env")


async def main_loop():
    check_update_api = 0
    coinsIds = await get_focus_coins_id();

    memMarket = MemMarketFollow(coinToFollow=coinsIds);

    # Allocate budget must be called EACH X times => not always
    # /force doit être déplacer dans une autre application ( autre API )
    await allocate_budget(coinbase_pro_client=CoinbaseConfiguration, asset_name="EUR")

    uri = "wss://ws-feed.exchange.coinbase.com" #"wss://ws-feed.prime.coinbase.com"
    async with websockets.connect(uri, ping_interval=None, max_size=None) as websocket:
        data = json.dumps({
            "type": "subscribe",
            "product_ids": coinsIds,
            "channels": [
                "l2update",
                {
                    "name": "ticker",
                    "product_ids": coinsIds
                }
            ]
        })
        await websocket.send(message=data)
        try:
            while True:
                resp = await websocket.recv()
                check_update_api += 1
                
                cleanup_signal = False
                if int(check_update_api == 0) or int(check_update_api) == int(extraConf["THICK_API_BUDGET"]):
                    cleanup_signal = True


                await dispatch(resp, memMarket, cleanup_signal)
                
                if int(check_update_api == 0) or int(check_update_api) == int(extraConf["THICK_API_BUDGET"]):
                    await allocate_budget(coinbase_pro_client=CoinbaseConfiguration, asset_name="EUR")
                    check_update_api = 0
                
        except websockets.exceptions.ConnectionClosedError:
            print("Error caught")

 

if __name__ == '__main__':
    asyncio.run(main=main_loop())

# Resource
# => https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccounts
# Interessting : https://www.youtube.com/watch?v=a74pQbHgdXw&t=375s


# 1 Get all money from DB (coinTarget)
# 2 Get from coinbase data about fund ( and check if we have enough ) for each coins
# 3 IF ok => start trading

# async def start_ws_client(app):
#     await allocate_budget(coinbase_pro_client=CoinbaseConfiguration, asset_name="EUR")

# def main():
#     # Out of async context
#     # asyncio.get_event_loop().run_until_complete(allocate_budget(coinbase_pro_client=CoinbaseConfiguration, asset_name="EUR"))

#     app = web.Application()
#     cors = aiohttp_cors.setup(app, defaults={
#         "*": aiohttp_cors.ResourceOptions(
#                 allow_credentials=True,
#                 expose_headers="*",
#                 allow_headers="*",
#             )
#     })

#     app.add_routes([web.post('/api/focus', add_focus_coin)])
#     app.on_startup.append(start_ws_client)
#     web.run_app(app)


# if __name__ ==  '__main__':
#     main()

