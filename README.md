
<!-- GETTING STARTED -->
## Getting Started

This is a project used as a stock screener for us stocks
### Web Screener
Filter based on WPR_2MA strategy, further classified as zacksRank 1 to 5(Strong buy - buy - hold - sell - Strong Sell) and Date of the signal
* Usage
  ```sh
  cd '.\Web Screener\'
  python app.py
  ```

### Daily
Daily update of zacksRank rank base on zacks-api, which is located at Database/signals.json
* Usage
  ```sh
  cd '.\Database\'
  ```
### Fourier Transformation(in progress)
Use fourier Transformation and trig approximation to predict stock price/direction
* Usage
  ```sh
  cd '.\Daily\'
  FFT_trigfit_con.py
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