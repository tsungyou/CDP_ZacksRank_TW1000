import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import scipy.stats as ss
# used inside fx_correlation()
def correlation(dataframe, type="spearman"):
    usd = dataframe.iloc[:, 0]
    eur = dataframe.iloc[:, 1]
    if type == "spearman":
        corr = ss.spearmanr(usd, eur)
    elif type == "pearson":
        corr = ss.pearsonr(usd, eur)
    elif type == "kendalltau":
        corr = ss.kendalltau(usd, eur)
    else:
        corr = ss.spearmanr(usd, eur)
    return corr.correlation

def fx_correlation(pairs=["USDCHF", "EURUSD"],type="spearman", data_type="Close", window_size=200):
    # data preprocessing
    currency1 = pairs[0]
    currency2 = pairs[1]
    try:
        pair1 = pd.read_csv(f"price/{currency1}=X.csv", index_col='Date')
        pair2 = pd.read_csv(f"price/{currency2}=X.csv", index_col="Date")
        print("Data Existed")
    except FileNotFoundError:
        path = "research/price/" + currency2 + ".csv"
        print(f".csv file doesn't exist, will create one inside {path}")
        start_date = datetime.datetime.today()- datetime.timedelta(4000) 
        end_date = datetime.datetime.today()
        a = yf.download(f"{currency1}=X", start=start_date, end=end_date)
        b = yf.download(f"{currency2}=X", start=start_date, end=end_date)
        a.to_csv("research/price/" + currency1 + ".csv")
        b.to_csv(path)
        print("successfully crerated")
        pair1 = pd.read_csv(f"price/{currency1}=X.csv", index_col='Date')
        pair2 = pd.read_csv(f"price/{currency2}=X.csv", index_col="Date")
        print("Data created and read")
    
    # concat data used, usually Close price only
    pair1[currency1] = pair1[data_type]
    pair2[currency2] = pair2[data_type]
    cl1 = pair1[[currency1]]
    cl2 = pair2[[currency2]]
    df = pd.concat([cl1, cl2], axis=1) # column-wise

    correlation_values = [np.nan] * (window_size-1)
    for i in range(window_size, len(df) + 1):
        window_data = df.iloc[i - window_size:i]
        corr_value = correlation(window_data, type=type)
        correlation_values.append(corr_value)
    # the way to solve the index problem
    corr_df = pd.DataFrame(correlation_values, index=usdchf.index, columns=["correlation"])
    df["correlation"] = corr_df[["correlation"]]
    # Access the correlation value for the last row of each window
    df = df.dropna()
    plt.plot(df[['correlation']])
    plt.title("spearman's correlation coefficient")

    xticks = df.index[::len(df.index)//10]  # Choose every 1/5th index
    plt.xticks(xticks, rotation=45)
    plt.show()
    return None

def main():
    return 0

if __name__ == "__main__":
    usdchf = pd.read_csv("price/USDCHF=X.csv", index_col='Date')
    eurusd = pd.read_csv("price/EURUSD=X.csv", index_col="Date")
    # for more https://realpython.com/numpy-scipy-pandas-correlation-python/
    usdchf_close = usdchf['Close'][:200] # ['Open'] with lower correlation
    eurusd_close = eurusd["Close"][:200] # 如果要嚴謹一點可以用 open 或是其他的
    pearson = np.corrcoef(usdchf_close, eurusd_close) # pearson's corrcoef
    pearsonr = ss.pearsonr(usdchf_close, eurusd_close)
    spearmanr = ss.spearmanr(usdchf_close, eurusd_close)
    kendalltau = ss.kendalltau(usdchf_close, eurusd_close)
    print(pearsonr) # = pearsonr.correlation
    print(spearmanr)
    print(kendalltau)
    # pandas
    usdchf_close.corr(eurusd_close) # shows person as default als0
    # => scipy.stats souble be better, which also provides with p-value
    main()