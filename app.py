from requests.auth import AuthBase
from dotenv import dotenv_values
from src.api.CoinMiddleware import add_focus_coin
from src.coinbase.Configuration import Configuration
from src.db.Configuration import Configuration as dbConfiguration
from src.services.FundService import allocate_budget
from aiohttp import web
import aiohttp_cors
import asyncio

CoinbaseConfiguration = Configuration(dotenv_values(".env"))
DbConfiguration = dbConfiguration(dotenv_values(".env"))

# Resource
# => https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccounts
# Interessting : https://www.youtube.com/watch?v=a74pQbHgdXw&t=375s


# 1 Get all money from DB (coinTarget)
# 2 Get from coinbase data about fund ( and check if we have enough ) for each coins
# 3 IF ok => start trading

async def start_ws_client(app):
    await allocate_budget(coinbase_pro_client=CoinbaseConfiguration, asset_name="EUR")

def main():
    # Out of async context
    # asyncio.get_event_loop().run_until_complete(allocate_budget(coinbase_pro_client=CoinbaseConfiguration, asset_name="EUR"))

    app = web.Application()
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    app.add_routes([web.post('/api/focus', add_focus_coin)])
    app.on_startup.append(start_ws_client)
    web.run_app(app)


if __name__ ==  '__main__':
    main()

