import requests
import statistics

#convert bitcoin price to USD
def btc_to_usd(price: str) -> str:  
    r = requests.get(f"https://www.okex.com/api/v5/market/index-components?index=BTC-USD").json()
    for i in r["data"]["components"]:
        bitcoin_price = float(i["symPx"])
        coin_price = bitcoin_price*float(price)
        return str(coin_price)

#convert USDT price to USD
def usdt_to_usd(price: str) -> str:
    r = requests.get("https://www.okex.com/api/v5/market/index-components?index=USDT-USD").json()
    for i in r["data"]["components"]:
        usdt_price = float(i["symPx"])
        coin_price = usdt_price*float(price)
        return str(coin_price)

#convert USDC price to USD
def usdc_to_usd(price: str) -> str:
    r = requests.get("https://www.okex.com/api/v5/market/index-components?index=USDC-USD").json()
    for i in r["data"]["components"]:
        usdc_usdt = float(i["symPx"])
        usdc_price = float(usdt_to_usd(usdc_usdt))
        coin_price = usdc_price*float(price)
        return str(coin_price)

#check if error is more than 3 or not   
def detect_error(price: list) -> list:
    error = price.count("error")
    if error >= 3:
        return []
    remove_error_price = [value for value in price if value != "error"]
    return remove_error_price

#filter an outlier data
def filter_data(data: list) -> list:
    status = []
    float_data = [float(value) for value in data]
    for value in float_data[1:]:
        percentage = float(data[0])/value*100   
        if 95 < percentage < 105:   #the data which out of the limit will be rejected 
            status.append(True)
        else:
            status.append(False)
    if True not in status:
        del data[0]
    elif False in status:
        false_index = status.index(False)
        del data[false_index]
    return data

#calculate median
def cal_median(data: list) -> str:
    float_data = [float(value) for value in data]
    return statistics.median(float_data)    
