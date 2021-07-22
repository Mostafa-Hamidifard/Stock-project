import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Indicator.indicator import Indicator
from datetime import datetime
import matplotlib.ticker as ticker


class MovingAverage(Indicator):
    def __init__(self, raw_data, rate=12, price_type="<LAST>"):
        Indicator.__init__(self, raw_data)
        self.dates = self.raw_data['<DTYYYYMMDD>'].values
        self.price = self.raw_data[price_type].values
        self.name = str(raw_data["<TICKER>"][0])
        self.rate = rate
        self.ma = self._calculate_mvaverage()

    def _calculate_mvaverage(self):
        mv_ave = np.convolve(self.price, np.ones(
            self.rate), 'valid') / self.rate
        a = np.empty(self.rate-1)
        a[:] = np.NaN
        return np.concatenate((a, mv_ave), axis=0)

    def get_dates(self):
        dates = self.dates
        return [datetime.strptime(str(i), '%Y%m%d').date() for i in dates]

    def plot(self, ax):
        x_value = self.get_dates()
        y_value = self.ma
        ax.set_title(self.name, fontsize=7)
        #    for scalable date formatted x axis
        N = len(self.price)
        ind = np.arange(N)

        def format_date(x, pos=None):
            thisind = np.clip(int(x + 0.5), 0, N - 1)
            plt.xticks(rotation=10)
            return x_value[thisind].strftime('%y-%m-%d')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

        lin1, = ax.plot(ind, y_value, linewidth=1)
        lin1.set_label("Moving Average"+f" ({self.rate} days)")
        ax.legend(fontsize='xx-small')
        ax.xaxis.set_tick_params(labelsize='xx-small')
        ax.yaxis.set_tick_params(labelsize='xx-small')


if __name__ == "__main__":
    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")
    # data = np.array([10, 5, 8, 9, 15, 22, 26, 11, 15, 16, 18, 7])
    df = df[::-1]
    fig = plt.figure(1, figsize=(6, 4), dpi=150, edgecolor='k')
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    mv1 = MovingAverage(df, 30)
    mv1.plot(ax1)
    ax1.grid()
    plt.show()
