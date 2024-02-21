from flask import Flask, render_template, request
import yfinance as yf
import json
import os
import pandas as pd
from datetime import datetime, timedelta
from config import sample, filemap
app = Flask(__name__)
route = "../Database/Tickers"
@app.route('/')
def hello_world():
    pattern = request.args.get("pattern", None)
    with open(filemap['SP500']):
        pass
    # if pattern:
    #     datafiles = os.listdir(route)
    #     for filename in datafiles:
    #         df = pd.read_csv(route + "/" + filename)
    #         # print(df.head())
    return render_template("index.html", patterns=sample)

@app.route('/snapshot')
def snapshot():
    return {
        "code": "success",
        "sucess": True,
        "message": "localhost:5000",
        "status": "200"
    }

if __name__ == "__main__":
    app.run(debug=True)
