import requests
from pprint import pprint

""" 
Using asset_name as "main" source for transaction

"""
def allocate_budget(coinbase_pro_client, asset_name):
    resp = requests.get(coinbase_pro_client.api_rest_base_url + 'accounts', auth=coinbase_pro_client)
    if resp.status_code == 200:
        target_asset = list(filter(lambda x: (x["currency"] == asset_name), resp.json()))
        pprint(target_asset[0])

    else:
        print("error")







# {'available': '100600',
#  'balance': '100600.0000000000000000',
#  'currency': 'EUR',
#  'hold': '0.0000000000000000',
#  'id': '6ef3d353-cc92-4c6a-9fff-7684e08ed499',
#  'profile_id': '3045f879-1957-4ec0-9eb8-819622d89e63',
#  'trading_enabled': True}