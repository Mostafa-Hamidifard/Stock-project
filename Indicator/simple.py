import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from indicator import Indicator
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.ticker as ticker


class Simple(Indicator):
    def __init__(self, raw_data, price_type="<LAST>"):
        Indicator.__init__(self, raw_data)
        self.price_type = price_type
        self.price = raw_data[price_type].values
        self.name = raw_data["<TICKER>"][0]

    def get_dates(self):
        df = self.raw_data
        dates = df["<DTYYYYMMDD>"].values
        return [datetime.strptime(str(i), '%Y%m%d').date() for i in dates]

    def plot(self, ax):
        ax.set_title(self.name, fontsize=7)
        x_value = self.get_dates()
        y_value = self.price
    #    for scalable date formatted x axis
        N = len(self.price)
        ind = np.arange(N)

        def format_date(x, pos=None):
            thisind = np.clip(int(x + 0.5), 0, N - 1)
            plt.xticks(rotation=10)
            return x_value[thisind].strftime('%y-%m-%d')
        (lin1,) = ax.plot(ind, y_value)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

        lin1.set_label(f"Simple({self.price_type.strip('<>').lower()})")
        ax.legend(fontsize="xx-small")
        ax.xaxis.set_tick_params(labelsize="xx-small")
        ax.yaxis.set_tick_params(labelsize="xx-small")


if __name__ == "__main__":
    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")[::-1]
    s = Simple(df)
    fig = plt.figure(1, figsize=(5, 3), dpi=150, edgecolor="k")
    ax1 = fig.add_axes([0.125, 0.125, 0.8, 0.8])
    s.plot(ax1)
    ax1.grid()
    # fig.autofmt_xdate()
    plt.show()
