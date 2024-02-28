from flask import Flask, render_template, request
import yfinance as yf
import json
import os
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from config import sample, filemap, datetime_dict, direction
app = Flask(__name__)
route = "../Database/Tickers"
@app.route('/')
def hello_world():
    pattern = request.args.get("pattern", "1")
    dat = request.args.get("datetime", "1")
    direct = request.args.get("direction", "2")
    database_type = request.args.get("database", "portfolio")
    data = {}
    change_daily = {}
    if database_type == "1":
        with open("../Database/zackRanks_portfolio.json", "r") as f:
            python_dict = json.load(f)
            for i in list(python_dict.keys()):
                data[i] = list(python_dict[i].values())
        print(data)
    elif database_type in ["2", "3"]:
        
        with open("../Database/signals.json", "r") as f:
            python_dict = json.load(f)
            day_dict = python_dict[datetime_dict[dat]][direction[direct]]
        if str(pattern) == "0":
            data = day_dict
        for key, val in day_dict.items():
            if str(val) == str(pattern):
                data[key] = pattern
        data = dict(sorted(data.items(), key=lambda item: item[1]))
        if database_type == "3":
            pass
        for ticker in data:
            a = yf.download(ticker, start=datetime.now()-timedelta(days=5), progress=False)
            percentage = f"{np.round((a['Close'][-1] - a['Close'][-2])/a['Close'][-2]*100, 2)}%"
            change_daily[ticker] = percentage
    # for key, val in day_dict.items():
    #     if str(val) == str(pattern):
    #         data[key] = val
    # print("data: ", data)
        
    return render_template("index.html", patterns=sample, datetime_dict = datetime_dict, stocks=data, direction=direction, change_daily=change_daily)
    # if pattern:

    #     datafiles = os.listdir(route)
    #     for filename in datafiles:
    #         df = pd.read_csv(route + "/" + filename)
    #         # print(df.head())
    # return render_template("index.html", patterns=sample, datetime_dict = datetime_dict, stocks=data)
@app.route('/tw')
def get_1000_tw():
    
    consecutive = request.args.get("consecutive", "1")
    with open("../Database/TW/TW50.json", "r") as f:
        python_dict = json.load(f)
    list_ = ["1513", "2330", "3037"]
    list_ = list(python_dict.keys())
    print(list_)
    nums = {}
    filtered_pairs = {}
    for stock in list_:
        date = []
        signal = []
        stock_dict = python_dict[stock]
        for key, value in stock_dict.items():
            date.append(key)
            signal.append(value['Signal'])
        
        index = next((i for i, x in enumerate(signal[::-1]) if x != 1), None)
        nums[stock] = index
    if consecutive == "1":
        for key, value in nums.items():
            if value != None:
                if 6 > value > 0:

                    filtered_pairs[key] = value
                else:
                    pass
        filtered_pairs = dict(sorted(filtered_pairs.items(), key=lambda item: item[1]))
        print(filtered_pairs)
    elif consecutive == "2":
        for key, value in nums.items():
            if value != None:
                if 10 > value >= 6:
                    filtered_pairs[key] = value
                else:
                    pass
        filtered_pairs = dict(sorted(filtered_pairs.items(), key=lambda item: item[1]))
        print(filtered_pairs)
    elif consecutive == "3":
        for key, value in nums.items():
            if value != None:
                if value > 10:
                    filtered_pairs[key] = value
                else:
                    pass
        filtered_pairs = dict(sorted(filtered_pairs.items(), key=lambda item: item[1]))
        print(filtered_pairs)
    return render_template("tw_1000.html", consecutive=consecutive, nums=filtered_pairs)

@app.route('/snapshot')
def snapshot():
    return {
        "code": "success",
        "sucess": True,
        "message": "localhost:5000",
        "status": "200"
    }

@app.route("/symbol")
def getSymbolInform():
    matplotlib.use("agg")
    symbol = request.args.get("symbol", "NVDA")
    df = pd.read_csv(f"../Database/Tickers/{symbol}.csv")
    plt.plot(df['Close'])
    return render_template("singleStock.html")
@app.route("/strat/wpr")
def strategy_wpr_2ma():
    return render_template("singleStock.html")


if __name__ == "__main__":
    app.run(debug=True)
