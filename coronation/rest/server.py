from aiohttp import web
import requests
from aiohttp.web_response import StreamResponse


async def health(request: StreamResponse):
    print(f"Request from {request.remote} for {request.url}")
    return web.Response(text="<h1> Async Rest API using aiohttp : Health OK </h1>",
                        content_type='text/html')


async def get_crypto_info(request):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    if response.status_code in [200, 201]:
        return web.Response(text=response.text, content_type='application/json')
    else:
        return web.Response(text=str({"status": "failure", "status_code": response.status_code}))


async def init():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_post("/v1/crypto/info", get_crypto_info)
    return app


if __name__ == "__main__":
    application = init()
    web.run_app(application, port=8000)