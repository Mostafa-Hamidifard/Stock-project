import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Indicator.indicator import Indicator
import math
from datetime import datetime
import matplotlib.ticker as ticker


class Normalize(Indicator):
    def __init__(self, raw_data, price_type="<LAST>"):
        Indicator.__init__(self, raw_data)
        self.name = raw_data["<TICKER>"][0]
        self.price = raw_data[price_type].values
        x_axis = np.linspace(0, self.price.size, self.price.size)
        temp = self.price - np.min(self.price)
        self.price = temp / np.max(temp)

    def get_dates(self):
        df = self.raw_data
        dates = df["<DTYYYYMMDD>"].values
        return [datetime.strptime(str(i), '%Y%m%d').date() for i in dates]

    def plot(self, ax):
        x_value = self.get_dates()
        y_value = self.price
        ax.set_title(self.name, fontsize=7)
  #    for scalable date formatted x axis
        N = len(self.price)
        ind = np.arange(N)

        def format_date(x, pos=None):
            thisind = np.clip(int(x + 0.5), 0, N - 1)
            plt.xticks(rotation=10)
            return x_value[thisind].strftime('%y-%m-%d')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        (lin1,) = ax.plot(ind, y_value, linewidth=1, color="green")
        lin1.set_label("Normalized")
        ax.legend(fontsize="xx-small")
        ax.xaxis.set_tick_params(labelsize="xx-small")
        ax.yaxis.set_tick_params(labelsize="xx-small")


if __name__ == "__main__":
    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")

    df = df[::-1]
    nm = Normalize(df)
    fig = plt.figure(1, figsize=(5, 3), dpi=150, edgecolor="k")
    ax1 = fig.add_axes([0.125, 0.125, 0.8, 0.8])
    nm.plot(ax1)
    ax1.grid()
    plt.show()
