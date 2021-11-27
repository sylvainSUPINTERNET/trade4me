import asyncio
from asyncio import exceptions
import websockets
import json
from aiohttp import web

async def handle(request):
    return web.Response(text="hello")


async def main_loop():
    uri = "wss://ws-feed.exchange.coinbase.com" #"wss://ws-feed.prime.coinbase.com"
    async with websockets.connect(uri, ping_interval=None, max_size=None) as websocket:
        data = json.dumps({
            "type": "subscribe",
            "product_ids": [
                "MANA-EUR"
            ],
            "channels": [
                "level2",
                "heartbeat",
                {
                    "name": "ticker",
                    "product_ids": [
                        "MANA-EUR"
                    ]
                }
            ]
        })
        await websocket.send(message=data)
        try:
            while True:
                resp = await websocket.recv()
                print(resp)
        except websockets.exceptions.ConnectionClosedError:
            print("Error caught")

 

if __name__ == '__main__':
    asyncio.run(main=main_loop())