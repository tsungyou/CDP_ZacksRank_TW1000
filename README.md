
<!-- GETTING STARTED -->
## Getting Started

fourier Transformation: Use fourier Transformation、trig approximation and Quinn and Fernandes algorithm to predict stock price

### Fourier Transformation
Use fourier Transformation and trig approximation to predict stock price/direction
* Usage
  ```sh
  cd '.\Daily\'
  FFT_trigfit_con.py
  ```


### Web Screener
Filter based on WPR_2MA strategy, further classified as zacksRank 1 to 5(Strong buy - buy - hold - sell - Strong Sell) and Date of the signal
Using javascrpit zacps-api + Windows Task manager to scrape zackRank everyday
* Usage
  ```sh
  cd '.\Web Screener\'
  python app.py
  ```

### CDP for us stock(2024-03-10 Update)
Revised CDP strategy for US stock
* Usage
  ```sh
  cd '.\Daily\'
  CDP_tech_test.ipynb
  ```

### Daily
Daily update of zacksRank rank base on zacks-api, which is located at Database/signals.json
* Usage
  ```sh
  cd '.\Database\'
  ```

### 台股大戶指標(in progress)
神秘金字塔(https://norway.twsthr.info/StockHolders.aspx)爬持股>1000張比例+股價、大戶持股兩條移動平均計算，如果兩組都滿足向上 ? signal = 1(buy): signal = 0
* Data location
  ```sh
  cd '.\Daily\TW\'
  TW50.json
  ```
* ipynb file location
  ```sh
  cd '.\Daily\'
  TW_stock_1000.ipynb
  ```