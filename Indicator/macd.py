from indicator import Indicator
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker


def EMA(x, days, smoothing=2):
    alpha = smoothing/(1+days)
    result = np.zeros(x.shape)
    result[0] = x[0]
    for i in range(1, x.size):
        result[i] = (1-alpha)*result[i-1]+alpha*x[i]
    return result


class MACD(Indicator):
    '''be aware, this class assumes that data is in reverse order, so it tries to reverse it again to make it in right order'''

    def __init__(self, raw_data, price_type="<LAST>", slow=26, fast=12, smooth=9):
        Indicator.__init__(self, raw_data)
        self.date = self.raw_data['<DTYYYYMMDD>'].values
        self.price = self.raw_data[price_type].values
        # processing data and computing macd line and signal line and histogram line
        self.name = raw_data["<TICKER>"][0]
        input = raw_data[price_type].values
        self.macd_line = EMA(input, fast) - \
            EMA(input, slow)
        self.signal_line = EMA(self.macd_line, smooth)
        self.histogram = self.macd_line - self.signal_line

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

        lin1, = ax.plot(ind, self.macd_line, linewidth=1)
        lin1.set_label("MACD line")
        lin2, = ax.plot(ind, self.signal_line, linewidth=1)
        lin2.set_label("Signal line")
        ax.legend(fontsize='xx-small')
        ax.fill_between(np.linspace(1, self.histogram.size,
                        self.histogram.size), self.histogram, 0, where=self.histogram >= 0, interpolate=True, facecolor='cyan')
        ax.fill_between(np.linspace(1, self.histogram.size,
                        self.histogram.size), self.histogram, 0, where=self.histogram < 0, interpolate=True, facecolor='#c3015c')
        ax.xaxis.set_tick_params(labelsize='xx-small')
        ax.yaxis.set_tick_params(labelsize='xx-small')


if __name__ == '__main__':
    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")[::-1]

    # sample code
    macd = MACD(df)
    fig = plt.figure(1, figsize=(5, 3), dpi=150, edgecolor='k')
    ax1 = fig.add_axes([0.125, 0.125, 0.8, 0.8])
    macd.plot(ax1)
    plt.show()
