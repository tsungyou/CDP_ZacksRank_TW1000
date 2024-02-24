from datetime import datetime, timedelta
import json

with open("../Database/signals.json") as f:
    a = json.load(f)
    time_keys = a.keys()
datetime_dict = {}
for i, times in enumerate(list(time_keys)[::-1]):
    datetime_dict[str(i+1)] = times

direction = {
    "2": "buy",
    "1": "sell" 
}
sample = {
    "1":"Strong Buy", 
    "2":"Buy",
    "3":"Hold",
    "4":"Sell",
    "5":"Strong Sell",
    "0": "All"
}

route = "../Database/"
filemap = {
    "NYSE"  : route + "../Database/zackRanks_NYSE.json", # 1352
    "NASDAQ": route + '../Database/zackRanks_NASDAQ.json', # small:1255; mid:330; large:72
    "SP500" : route + "../Database/zackRanks_SP500.json", # small: 1352
   "Yuanta": route + "zackRanks_yuanta.json",
   "buy": route + "buy.json",
   "sell": route + "sell.json",
   "portfolio": route + "zackRanks_portfolio.json"
}