import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

db_location = "../Database/TW/TW50/TW50.json"


def insert_db_new(ticker):
    with open(db_location, encoding='utf-8') as f:
        dicts = json.load(f)
    



def insert_db_update(ticker):
    pass
