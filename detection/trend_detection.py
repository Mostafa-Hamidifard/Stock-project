import pandas as pd
import numpy as np
from numpy import linalg
from matplotlib import pyplot as plt


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def detect_trend(raw_data, fromthis, tothis=-1, end=False, price_type="<LAST>"):
    '''
    inputs: raw_data as data frame
            fromthis -> from this position untill end (usually negative)
            price_type='<LAST>'
    returns : detection(as string), m(slope), c(constant)
    '''
    if end:
        price = raw_data[price_type].values[-fromthis:]
        length = len(raw_data) - fromthis
    else:
        price = raw_data[price_type].values[fromthis:tothis]
        length = tothis - fromthis
    if length > 40:
        price = moving_average(price, 20)
    x_axis = np.linspace(0, 1, price.size)
    price = price - np.min(price)
    price = price/np.max(price)
    A = np.vstack([x_axis, np.ones(len(x_axis))]).T
    m, c = linalg.lstsq(A, price, rcond=None)[0]
    ref = np.tan(20 * np.pi/180)
    if(m > ref):
        return "Ascending", m, c
    elif(m < -ref):
        return "Descending", m, c
    else:
        return 'No trend', m, c


if __name__ == '__main__':
    df = pd.read_csv(
        "E:\\ap_final\\Stock-project\\CSV raw data\\2400322364771558.csv")
    df = df[::-1]
    price = df["<CLOSE>"].values[40:150]
    x_axis = np.linspace(0, 1, price.size)
    price = price - np.min(price)
    price = price/np.max(price)
    detection, m, c = detect_trend(df, 40, 150)
    y = m*x_axis + c
    print(detection)
    plt.plot(x_axis, y)
    plt.plot(x_axis, price)
    plt.show()
