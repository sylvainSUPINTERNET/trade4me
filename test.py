# Example using coinbase ( not pro ), means account maangement etc ( like OAUTH2)

# import json, hmac, hashlib, time, requests
# from requests.auth import AuthBase
# from dotenv import dotenv_values
# import pprint
# config = dotenv_values(".env")

# # Before implementation, set environmental variables with the names API_KEY and API_SECRET
# API_KEY = config["API_KEY"]
# API_SECRET = config["API_SECRET"]
# API_VERSION = config["API_VERSION"]


# # Create custom authentication for Coinbase API
# class CoinbaseWalletAuth(AuthBase):
#     def __init__(self, api_key, secret_key, api_version):
#         self.api_key = api_key
#         self.secret_key = secret_key
#         self.api_version = api_version

#     def __call__(self, request):
#         timestamp = str(int(time.time()))

#         # the following try statement will fix the bug
#         try:
#             body = request.body.decode()
#             if body == "{}":
#                 request.body = b""
#                 body = ''
#         except AttributeError:
#              request.body = b""
#              body = ''

#         message = timestamp + request.method + request.path_url + body
#         signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
#         request.headers.update({
#                 'CB-ACCESS-SIGN': signature,
#                 'CB-ACCESS-TIMESTAMP': timestamp,
#                 'CB-ACCESS-KEY': self.api_key,
#                 'CB-VERSION': self.api_version
#         })
#         return request


# api_url = 'https://api.coinbase.com/v2/'
# auth = CoinbaseWalletAuth(API_KEY, API_SECRET, API_VERSION)

# # Get current user
# r = requests.get(api_url + 'user', auth=auth)
# r2 = requests.get(api_url + 'accounts', auth=auth) # get for each asset 
# r3 = requests.get(api_url + "accounts/MANA", auth=auth) # get wallet for KEEP asset only
# r4 = requests.get(api_url + "accounts/EUR", auth=auth) # get wallet for KEEP asset only


# pprint.pprint(r3.json())
# pprint.pprint(r4.json())
