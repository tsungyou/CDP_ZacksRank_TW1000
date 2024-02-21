from datetime import datetime, timedelta

datetime_dict = {
    "1": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "2": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
    "3": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
    "4": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
    "5": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
}

direction = {
    "1": "sell",
    "2": "buy" 
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