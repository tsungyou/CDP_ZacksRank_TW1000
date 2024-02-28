import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import tqdm

db_location = "../Database/TW/TW50.json"
default = "2330"

def get_1000_data(ticker=default):
    url = f"https://norway.twsthr.info/StockHolders.aspx?stock={ticker}"
    c = requests.get(url)
    soup = BeautifulSoup(c.text, "lxml")
    ds = soup.find_all("tr", {"class":"lDS"})
    ls = soup.find_all("tr", {"class":"lLS"})

    title = []
    date_ds = []
    date_ls = []
    price_ds = []
    price_ls = []
    percentage_ls = []
    percentage_ds = []
    total = 166 + 1
    total_ds = 83+1
    total_ls = 83

    for cc, i in enumerate(ds):
        for q, k in enumerate(i):
            if cc != 0:
                if q == 2:
                    date_str = k.text[:-1]
                    date_ds.append(f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}")
                if q == 13:
                    percentage_ds.append(k.text)
                if q == 14:
                    price_ds.append(k.text)

            else:
                if q in [2, 13, 14]:
                    title.append(k.text)
        if cc >= total_ds + 1:
            break

    for cc, i in enumerate(ls):
        for q, k in enumerate(i):
            if q == 2:
                date_str = k.text[:-1]
                date_ls.append(f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}")
            if q == 13:
                percentage_ls.append(k.text)
            if q == 14:
                price_ls.append(k.text)
        if cc >= total_ds + 1:
            break
    final_per = []
    final_pri = []
    final_dat = []
    for i in range(len(date_ds)): # 85 
        final_per.append(percentage_ds[i])
        final_per.append(percentage_ls[i])
        final_pri.append(price_ds[i])
        final_pri.append(price_ls[i])
        final_dat.append(date_ds[i])
        final_dat.append(date_ls[i])

    dates = [datetime.strptime(date, "%Y-%m-%d") for date in final_dat]

    # Convert values to float
    values = [float(value) for value in final_pri]
    percenta = [float(value) for value in final_per]
    return dates[::-1], values[::-1], percenta[::-1]



def insert_db_new():
    with open(db_location, "r", encoding="utf-8") as f:
        dicts = json.load(f)
    
    with tqdm.tqdm(total=len(list(dicts.keys()))) as pbar: 
    
        for ticker in list(dicts.keys()):
            try:
                dates, values, percenta = get_1000_data(ticker)
                for i, date in enumerate(dates):
                    dicts[ticker][date.strftime("%Y-%m-%d")] = {"Close":values[i], "Percent":percenta[i]}
            except:
                pass
            pbar.update(1)
        else:
            print(ticker, "failed")
    # print(dicts[ticker])
    with open(db_location, "w", encoding='utf-8') as f:
        json.dump(dicts, f, indent=4)
    return None

def insert_db_update(ticker=default):
    with open(db_location, "r", encoding="utf-8") as f:
        dicts = json.load(f)

    with tqdm.tqdm(total=len(list(dicts.keys()))) as pbar: 
        for ticker in list(dicts.keys()):
            try:
                dates, values, percenta = get_1000_data(ticker)
                dicts[ticker][dates[-1].strftime("%Y-%m-%d")] = {"Close":values[-1], "Percent":percenta[-1]}
            except:
                print(ticker, "failed")
            pbar.update(1)
        else:
            print(ticker, "failed")
    with open(db_location, "w", encoding='utf-8') as f:
        json.dump(dicts, f, indent=4)
    return None

def main():
    insert_db_new()
    # insert_db_update()
if __name__ == '__main__':
    main()