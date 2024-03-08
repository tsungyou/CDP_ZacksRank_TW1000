# Update json files for zackRanks raw files
# Daily Looping
from backtesting import Backtest, Strategy
import yfinance as yf
import json
import pandas as pd
import datetime
# import pandas_ta as ta
import tqdm
import subprocess
route = ""
filemap = {
    "NYSE"  : route + "../Database/zackRanks_NYSE.json", # 1352
    "NASDAQ": route + '../Database/zackRanks_NASDAQ.json', # small:1255; mid:330; large:72
    "SP500" : route + "../Database/zackRanks_SP500.json", # small: 1352
   "Yuanta": route + "zackRanks_yuanta.json",
   "portfolio": route + "zackRanks_portfolio.json"
}

def mains(today=0, loops = ["NYSE", "NASDAQ", "SP500"]):
    for k in loops:
        print("*"*20, k, "*"*20)
        with open(filemap[k], 'r') as f:
            python_dict = json.load(f)
            a = list(python_dict.keys())
            with tqdm.tqdm(total=len(a)) as pbar:
                for ticker in a:
                    try:
                        command = "zacks-api " + ticker
                        result = subprocess.check_output(command, shell=True)
                        result_decoded = result.decode("utf-8")
        # Parse the result as JSON
                        dict = json.loads(result_decoded)
                        tick = dict["ticker"]
                        rank = dict["zacksRank"]
                        if today == 0:
                            dat = dict["updatedAt"].split("T")[0]
                        else:
                            dat = datetime.datetime.now() - datetime.timedelta(days=today)
                        python_dict[tick][dat] = rank
                    except:
                        print(f"{ticker} passed")
                        pass
                    pbar.update(1)

        with open(filemap[k], 'w') as f:
            json.dump(python_dict, f, indent=4)

# Daily Looping FOR SIGNALS.JS
def get_tickers(file="SP500"):
    dict = pd.read_csv(filemap[file], header=None)
    dict = dict.iloc[:, 0]
    return dict

def WPRbt(data):
    period = 12
    max = data.Close.rolling(period).max()
    min = data.Close.rolling(period).min()
    wpr = (max - data.Close)/(max - min) * (-100) 
    return wpr

def check_WPR_2MA_without_DB(ticker, test=False, period_long_ma=28, period_short_ma=14, upb=-20, lob=-80):
    a = yf.download(ticker, start=datetime.datetime.now() - datetime.timedelta(days=50), interval="1d", progress=False)

    # a["WPR"] = WPRbt(a)
    a["MAX"] = a.High.rolling(12).max()
    a["MIN"] = a.Low.rolling(12).min()
    a["WPRs"] = (a.MAX - a.Close)/(a.MAX - a.MIN) * (-100)
    a["long_MA"] = a.Close.ewm(span=period_long_ma, adjust=False, min_periods=period_long_ma).mean()
    a['short_MA'] = a.Close.ewm(span=period_short_ma, adjust=False, min_periods=period_short_ma).mean()
    long0 = list(a['long_MA'])[-1]
    long1 = list(a['long_MA'])[-2]
    long2 = list(a['long_MA'])[-3]
    long3 = list(a['long_MA'])[-4]
    # =======================
    short0 = list(a['short_MA'])[-1]
    short1 = list(a['short_MA'])[-2]
    short2 = list(a['short_MA'])[-3]
    short3 = list(a['short_MA'])[-4]
    # =======================
    wpr0 = list(a['WPRs'])[-1]
    wpr1 = list(a['WPRs'])[-2]
    wpr2 = list(a['WPRs'])[-3]
    wpr3 = list(a['WPRs'])[-4]
    check_ma_percent = 0.0000# for PAYX at 2024-02-08, 0.005 return 4(meaning doesn't work ) while 0.006 works
    bear_market = (long0 - short0 > long0*check_ma_percent) and (long1 - short1 > long1*check_ma_percent) and (long2 - short2 > long2*check_ma_percent)
    bull_market = (long0 - short0 < long0*-check_ma_percent) and (long1 - short1 < long1*-check_ma_percent) and (long2 - short2 < long2*-check_ma_percent)
    if test:
        print(a[['Close', "short_MA", "long_MA", "WPRs", "MAX"]])
        print(wpr0, wpr1, wpr2, wpr3)
        print("quick: ", [short3, short2, short1, short0])
        print("slow: ", [long3, long2, long1, long0])
    # current signal
    if((wpr0 < upb) and (wpr1 > upb) and bear_market):
        # sell signal
        return 1
    elif ((wpr0 > lob) and (wpr1 < lob)) and bull_market:
        # buy signal
        return 2
    # check for yesterday or the day before yesterday buy/sell signal
    elif((wpr1 < upb) and (wpr2 > upb) and bear_market):
        return 1.5
    elif((wpr1 > lob) and (wpr2 < lob) and bull_market):
        return 2.5
    elif((wpr2 > lob) and (wpr3 < lob) and bull_market) or ((wpr2 > upb) and (wpr3 < upb) and bear_market):
        return 3

    else:
        return 0

def mains_signals_update(loops = ["NYSE", "NASDAQ", "SP500"]):
    sell_of_the_day = []
    buy_of_the_day = []
    all_signals_buy = {}
    all_signals_sell = {}
    for k in loops:

        print("*"*20, k, "*"*20)

        with open(filemap[k], 'r') as f:
            python_dict = json.load(f)
        a = list(python_dict.keys())
        if k in ['portfolio', "SP500", "Yuanta"]:
            tickers = a[:] 
        elif k == "NYSE":
            tickers = a[1:1352]
        elif k == "NASDAQ":
            tickers = a[1:1255]

        # Using tqdm to add a progress bar
        with tqdm.tqdm(total=len(tickers)) as pbar:
            res = {}
            for ticker in tickers:
                res[ticker] = check_WPR_2MA_without_DB(ticker)
                pbar.update(1)
                
        s = [{i:res[i]} for i in res.keys() if res[i] != 0 ]
        if sum(list(res.values())) == 0:
            print("there's nothing with signal")

        checks = [1, 2]
        for check in checks:
            q = [i for i in res.keys() if res[i] == check]
            dict_res = {}
            print(len(q))
            for ticker in q:
                try:
                    command = "zacks-api " + ticker
                    result = subprocess.check_output(command, shell=True)
                    dict = eval(result.decode(("utf-8"))) 
                    dict_res[ticker] = dict['zacksRank']
                    if check == 1:
                        sell = [ticker for ticker in list(dict_res.keys()) if dict_res[ticker] == "4"]
                        strong_sell = [ticker for ticker in list(dict_res.keys()) if dict_res[ticker] == "5"]
                        sell_of_the_day += strong_sell
                        all_signals_sell = {**all_signals_sell, **dict_res}
                    if check == 2:
                        strong_buy = [ticker for ticker in list(dict_res.keys()) if dict_res[ticker] == "1"]
                        buy = [ticker for ticker in list(dict_res.keys()) if dict_res[ticker] == "2"]
                        hold_but_signal = [ticker for ticker in list(dict_res.keys()) if dict_res[ticker] == "3"]
                        buy_of_the_day += strong_buy
                        all_signals_buy = {**all_signals_buy, **dict_res}
            # print(json.dumps(dict_res, indent=4))
                except:
                    print(ticker, "passed")
            print("=============")

    time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")


    with open("../Database/signals.json", "r") as f:
        ks = json.load(f)
    ks[time] = {"buy": all_signals_buy, "sell": all_signals_sell} 
    with open("../Database/signals.json", "w") as f:
        json.dump(ks, f , indent=4)

    print("Sell: ", sell_of_the_day)
    print("Buy: ", buy_of_the_day)
    print("Hold: ", hold_but_signal)
    print({"buy": all_signals_buy, "sell": all_signals_sell})





if __name__ == "__main__":
    loops = ["SP500", "NYSE", "NASDAQ"]
    mains(today=0, loops=loops)
    mains_signals_update(loops=loops)
