import requests
from pprint import pprint
from src.db.Configuration import Configuration as dbConfiguration
from dotenv import dotenv_values

""" 
Using asset_name as "main" source for transaction

"""
async def allocate_budget(coinbase_pro_client, asset_name):
    db = dbConfiguration(dotenv_values(".env"))

    print("ok")


    resp = requests.get(coinbase_pro_client.api_rest_base_url + 'accounts', auth=coinbase_pro_client)
    if resp.status_code == 200:
        target_asset = list(filter(lambda x: (x["currency"] == asset_name), resp.json()))
        focus = [i for i in db.get_collection("focus").find()]



        # TODO : 
        # Infos viennent du WS => product ID focus coinUse coinTarget
        # ensuite regarder buyer seller => si ça amtch avec le budget allouer si oui faire une première transaction
        # 


        # STEP 1 : Validate focus budget, related with market values

        # Budget available ( in currency chosen, especially EUR)
        # available = target_asset[0].available
        # balance = target_asset[0].balance
        # balance = target_asset[0].hold
        


        # pprint(focus)
        # pprint(target_asset[0])

    else:
        print("error")







# {'available': '100600',
#  'balance': '100600.0000000000000000',
#  'currency': 'EUR',
#  'hold': '0.0000000000000000',
#  'id': '6ef3d353-cc92-4c6a-9fff-7684e08ed499',
#  'profile_id': '3045f879-1957-4ec0-9eb8-819622d89e63',
#  'trading_enabled': True}