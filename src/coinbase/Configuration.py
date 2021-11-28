from requests.auth import AuthBase
import time
import hmac, hashlib, time
import base64

class Configuration(AuthBase):
    def __init__(self, config):
        self.api_key = config["API_KEY"]
        self.secret_key = config["API_SECRET"]
        self.api_version = config["API_VERSION"]
        self.passphrase = config["PASSPHRASE"]
        self.api_rest_base_url = config["API_REST_BASE_URL"]

    def __call__(self, request):
        timestamp = str(int(time.time()))
        try:
            body = request.body.decode()
            if body == "{}":
                request.body = b""
                body = ''
        except AttributeError:
             request.body = b""
             body = ''

        message = timestamp + request.method + request.path_url + body
        key = base64.b64decode(self.secret_key)
        signature = base64.b64encode(hmac.new(key, message.encode(), hashlib.sha256).digest())

        request.headers.update({
                'CB-ACCESS-SIGN': signature,
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-KEY': self.api_key,
                'CB-ACCESS-PASSPHRASE': self.passphrase,
                'CB-VERSION': self.api_version
        })
        return request
