import json
import requests
import wrapper
import calculator

#insert a list in one straight line
n = input("Please insert a list here >>> ")
input_ = json.loads(n)

coins_value = []
for coin in input_:
    five_price = wrapper.call_api(coin) #get a list of five price from wrapper.py
    checked_error = calculator.detect_error(five_price) #check if error is more than 3
    if checked_error == []:     
        coins_value.append("error")
        continue
    remove_outlier = calculator.filter_data(checked_error)  #filter outlier data
    get_median = calculator.cal_median(remove_outlier)  #calculate median
    coins_value.append(get_median)
print(coins_value)
