import pandas as pd
import ta
import matplotlib.pyplot as plt


class BacktestEngine:
    def __init__(self, data, trade_amount=10000):
        self.data = data
        self.positions = []
        self.trade_amount = trade_amount

    def buy(self, date, signal):
        self.positions.append((date, "buy", signal))

    def sell(self, date, signal):
        self.positions.append((date, "sell", signal))

    def process_signals(self, signals):
        # Initialize the 'Signal' column in the data DataFrame
        self.data["Signal"] = 0

        # Iterate through the signals DataFrame and update the 'Signal' column in the data DataFrame
        for date, signal in signals.iterrows():
            if signal["Signal"] == 1:
                self.buy(date, signal["Signal"])
            elif signal["Signal"] == -1:
                self.sell(date, signal["Signal"])
            self.data.loc[date, "Signal"] = signal["Signal"]

    def run_backtest(self, strategy_function, strategy_params=None):
        if strategy_params is None:
            strategy_params = {}

        signals = strategy_function(self.data, **strategy_params)

        self.process_signals(signals)
        performance = self.calculate_performance()

        return performance

    def calculate_performance(self):
        performance = pd.DataFrame(index=self.data.index, columns=["Value"])
        position = 0
        cash = self.trade_amount

        for date, row in self.data.iterrows():
            if len(self.positions) > 0 and self.positions[0][0] == date:
                _, action, signal = self.positions.pop(0)
                if action == "buy":
                    shares_to_buy = cash // row["Close"]
                    position += shares_to_buy
                    cash -= shares_to_buy * row["Close"]
                elif action == "sell":
                    cash += position * row["Close"]
                    position = 0

            performance.loc[date, "Value"] = position * row["Close"] + cash

        return performance

    def plot(self, performance, filename="performance_plot.png"):
        fig, ax1 = plt.subplots()

        ax1.plot(self.data.index, self.data["Close"], label="Close Price")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Stock Price")
        ax1.legend(loc="upper left")

        ax2 = ax1.twinx()
        ax2.plot(
            performance.index,
            performance["Value"],
            color="orange",
            label="Portfolio Value",
        )
        ax2.set_ylabel("Portfolio Value")
        ax2.legend(loc="upper right")

        plt.title("Stock Price and Portfolio Performance")
        plt.savefig(filename)
        plt.close(fig)


def moving_average_crossover_ema(data, short_window=50, long_window=200):
    # Calculate EMA
    ema_short = data["Close"].ewm(span=short_window).mean()
    ema_long = data["Close"].ewm(span=long_window).mean()

    # Calculate RSI
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"]).rsi()

    # Calculate MACD
    macd_ind = ta.trend.MACD(data["Close"])
    data["MACD"] = macd_ind.macd()
    data["MACD_signal"] = macd_ind.macd_signal()
    data["MACD_diff"] = macd_ind.macd_diff()

    signals = pd.DataFrame(index=data.index)
    signals["Signal"] = 0

    # Find buy and sell signals
    for i in range(1, len(data)):
        if (
            ema_short[i - 1] < ema_long[i - 1]
            and ema_short[i] > ema_long[i]
            and data["RSI"][i] < 80 # TODO: keep an eye on this
            and data["MACD_diff"][i] > 0
        ):
            signals.loc[data.index[i], "Signal"] = 1
        elif (
            ema_short[i - 1] > ema_long[i - 1]
            and ema_short[i] < ema_long[i]
            and data["RSI"][i] > 20 # TODO: keep an eye on this
            and data["MACD_diff"][i] < 0
        ):
            signals.loc[data.index[i], "Signal"] = -1

    return signals
