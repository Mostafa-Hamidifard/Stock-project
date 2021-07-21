import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Indicator.indicator import Indicator


class MovingAverage(Indicator):
    def __init__(self, raw_data, rate, price_type="<LAST>"):
        Indicator.__init__(self, raw_data[price_type].values)
        self.name = str(raw_data["<TICKER>"][0])
        self.ma = self._calculate_mvaverage(rate)
        self.rate = rate

    def _calculate_mvaverage(self, rate):
        mv_ave = np.convolve(self.raw_data, np.ones(rate), 'valid') / rate
        return np.concatenate((np.ones(rate-1)/0, mv_ave), axis=0)

    def plot(self, ax):
        ax.set_title(self.name, fontsize=7)
        lin1, = ax.plot(self.ma, linewidth=1)
        lin1.set_label("Moving Average"+f" ({self.rate} days)")
        ax.legend(fontsize='xx-small')
        ax.xaxis.set_tick_params(labelsize='xx-small')
        ax.yaxis.set_tick_params(labelsize='xx-small')


if __name__ == "__main__":
    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")
    # data = np.array([10, 5, 8, 9, 15, 22, 26, 11, 15, 16, 18, 7])
    mv = MovingAverage(df[::-1], 4)
    fig = plt.figure(1, figsize=(6, 4), dpi=150, edgecolor='k')
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    mv1 = MovingAverage(df[::-1], 30)
    mv1.plot(ax1)
    mv.plot(ax1)
    ax1.grid()
    plt.show()
