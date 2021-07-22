import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Indicator.indicator import Indicator
import math
from datetime import datetime
import matplotlib.ticker as ticker


def get_sma(raw_data, rate):
    mv_ave = np.convolve(raw_data, np.ones(rate), "valid") / rate
    a = np.empty(rate-1)
    a[:] = np.NaN
    return np.concatenate((a, mv_ave), axis=0)


class BBolinger(Indicator):

    def get_std(self, raw, sma, rate):
        # self.sma mean
        std = np.zeros(raw.size)
        std[0:rate-1] = np.NaN
        for i in range(rate-1, raw.size):
            # i=5 -> a = raw[5-5:5]==> raw[0:5] 0,1,2,3,4
            a = raw[i+1-rate:i+1]
            # a-self.sma[5] -> sma = [nan,nan,nan,nan,12,13]
            b = a - sma[i]  # i=raw.size-1
            b = b * b
            c = np.sum(b, dtype=np.float32)/rate
            std[i] = math.sqrt(c)
        return std

    def __init__(self, raw_data, price_type="<LAST>", rate=20, mult=2):
        Indicator.__init__(self, raw_data)
        self.name = raw_data["<TICKER>"][0]

        self.date = self.raw_data['<DTYYYYMMDD>'].values
        self.price = self.raw_data[price_type].values
        self.mult = mult
        self.rate = rate
        # processing
        self.sma = get_sma(self.price, rate)
        self.df = pd.DataFrame(self.price)
        self.std = self.get_std(self.df.values[:, 0], self.sma, rate)
        self.bollinger_up = self.sma + self.std * mult
        self.bollinger_down = self.sma - self.std * mult

    def get_dates(self):
        df = self.raw_data
        dates = df["<DTYYYYMMDD>"].values
        return [datetime.strptime(str(i), '%Y%m%d').date() for i in dates]

    def plot(self, ax):
        x_value = self.get_dates()
        ax.set_title(self.name, fontsize=7)
        #    for scalable date formatted x axis
        N = len(self.price)
        ind = np.arange(N)

        def format_date(x, pos=None):
            thisind = np.clip(int(x + 0.5), 0, N - 1)
            plt.xticks(rotation=10)
            return x_value[thisind].strftime('%y-%m-%d')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

        lin1, = ax.plot(ind, self.sma, linewidth=1, color='red', alpha=0.5)
        lin1.set_label(f"BB's SMA ({self.rate} days)")
        ax.legend(fontsize='xx-small')
        ax.fill_between(ind, self.bollinger_down, self.bollinger_up,
                        color="cyan", interpolate=True, edgecolor='blue', alpha=0.5)
        ax.xaxis.set_tick_params(labelsize='xx-small')
        ax.yaxis.set_tick_params(labelsize='xx-small')


if __name__ == "__main__":
    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")
    df = df[::-1]
    bb = BBolinger(df, rate=20)
    fig = plt.figure(1, figsize=(5, 3), dpi=150, edgecolor='k')
    ax1 = fig.add_axes([0.125, 0.125, 0.8, 0.8])
    bb.plot(ax1)
    ax1.grid()
    plt.show()

