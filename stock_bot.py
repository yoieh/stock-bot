import numpy as np
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

# import plotly.express as px
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output

import matplotlib.pyplot as plt

from alpha_vantage_handler import get_historical_data

from backtest import (
    BacktestEngine,
    moving_average_crossover_ema,
)


load_dotenv()


data = get_historical_data("MSFT")
engine = BacktestEngine(data)
performance = engine.run_backtest(
    moving_average_crossover_ema, {"short_window": 50, "long_window": 200}
)

print(performance)

engine.plot(performance)
