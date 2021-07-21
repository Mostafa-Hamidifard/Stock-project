import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from indicator import Indicator
import math


class Normalize(Indicator):
    def __init__(self, raw_data, price_type="<LAST>"):
        Indicator.__init__(self, raw_data)
        self.name = raw_data["<TICKER>"][0]
        self.price = raw_data[price_type].values
        x_axis = np.linspace(0, self.price.size, self.price.size)
        temp = self.price - np.min(self.price)
        self.price = temp / np.max(temp)

    def plot(self, ax):
        ax.set_title(self.name, fontsize=7)
        (lin1,) = ax.plot(self.price, linewidth=1, color="green")
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
