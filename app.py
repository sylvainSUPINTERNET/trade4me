from requests.auth import AuthBase
from dotenv import dotenv_values
from src.api.CoinMiddleware import add_focus_coin
from src.coinbase.Configuration import Configuration
from src.db.Configuration import Configuration as dbConfiguration
from src.services.FundService import allocate_budget
from aiohttp import web
import aiohttp_cors


CoinbaseConfiguration = Configuration(dotenv_values(".env"))
DbConfiguration = dbConfiguration(dotenv_values(".env"))

# Resource
# => https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccounts
# Interessting : https://www.youtube.com/watch?v=a74pQbHgdXw&t=375s

allocate_budget(coinbase_pro_client=CoinbaseConfiguration, asset_name="EUR")


app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

app.add_routes([web.post('/api/focus', add_focus_coin)])
web.run_app(app)

# async def handler(request):
#     return web.Response(text="Hello!")

# app = web.Application()
# cors = aiohttp_cors.setup(app)

# resource = cors.add(app.router.add_resource("/hello"))
# route = cors.add(resource.add_route("GET", handler))
""" 

Obj : 

=> Tell bot to use main fund ( FIAT such as EUR) for each money 
=> allocate budget (ex : 10 euros MAX for MANA / 1 euros max for CGLD ...)
=> Bot must be able to : 
===> buy alone (create a new order ) when price is interessting ( red )
===> Sell when the price is higher ( compare on history ) and interessting ( integrate fee price in transaction )

"""