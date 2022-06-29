import requests
import time
import calculator

#call Binance API
def binance(coin: str) -> str:
    url = f"https://api.binance.com/api/v3/avgPrice?symbol={coin}USDT"
    r = requests.get(url).json()
    if 'code' in r:
        url = f"https://api.binance.com/api/v3/avgPrice?symbol={coin}USDC"
        r = requests.get(url).json()
        if 'code' in r:
            return "error"
        price = calculator.usdc_to_usd(r["price"])
        return price
    return r["price"]

#call CoinGecko API
def coingecko(coin: str) -> str:
    coin = coin.lower()
    search_url = f"https://api.coingecko.com/api/v3/search?query={coin}"
    r = requests.get(search_url).json()
    if r["coins"] != [] and r["coins"][0]["symbol"] == coin.upper():
        coin_id = r["coins"][0]["id"]
        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        r = requests.get(price_url).json()
        return r[coin_id]["usd"]
    return "error"

#call CoinMarketCap API
def coinmarketcap(coin: str) -> str:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
      'symbol':coin,
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '33fd2723-baa9-4ff9-815c-ab5232374a1e',
    }    
    r = requests.get(url, params=params, headers=headers).json()
    if coin == "NCASH":
        coin = "NCash"
    if len(r["data"]) == 0 or r["data"][coin]["total_supply"] == None:
        return "error"
    else:
        return r["data"][coin]["quote"]["USD"]["price"]
#call Kraken API
def kraken(coin: str) -> str:
    r = requests.get(f"https://api.kraken.com/0/public/Ticker?pair={coin}USD").json()
    if r["error"] != []:
        return "error"
    name = list(r["result"])[0]
    return r["result"][name]["a"][0]

##call Okex API
def okx(coin: str) -> str:
    r = requests.get(f"https://www.okex.com/api/v5/market/index-components?index={coin}-USD").json()
    if r["code"] == '0':
        for i in r["data"]["components"]:
            if i["symbol"] == f"{coin}/USD" or i["symbol"] == f"{coin}/USDT":
                return i["symPx"]
            elif i["symbol"] == f"{coin}/BTC":
                return calculator.btc_to_usd(i["symPx"])
    else:
        return "error"

#call 5 APIs
def call_api(coin: str) -> list:
    five_price = []
    five_price.append(binance(coin))
    five_price.append(coingecko(coin))
    five_price.append(coinmarketcap(coin))
    five_price.append(kraken(coin))
    five_price.append(okx(coin))
    return five_price
    
