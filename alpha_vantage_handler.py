import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")


def get_stock_data(symbol):
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    ts = TimeSeries(key=api_key)
    data, _ = ts.get_quote_endpoint(symbol=symbol)
    return data


def get_historical_data(symbol):
    api_key = "your_api_key"
    ts = TimeSeries(key=api_key, output_format="pandas")
    data, _ = ts.get_daily_adjusted(symbol=symbol, outputsize="full")
    data = data.rename(
        columns={"4. close": "Close", "5. adjusted close": "Adjusted Close"}
    )
    return data
