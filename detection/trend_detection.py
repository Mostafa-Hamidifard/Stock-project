import pandas as pd
import numpy as np
from numpy import linalg
from matplotlib import pyplot as plt


def detect_trend(raw_data, fromthis, price_type="<CLOSE>", reverse=True):
    '''
    inputs: raw_data as data frame (set reverse=false if you have reversed it before)
            fromthis -> from this position untill end (usually negative)
            price_type='<CLOSE>'
    returns : detection(as string), m(slope), c(constant)
    '''
    price = np.flipud(raw_data[price_type].values)[fromthis:100]
    x_axis = np.linspace(0, 1, price.size)
    price = price - np.min(price)
    price = price/np.max(price)
    # print(price)
    A = np.vstack([x_axis, np.ones(len(x_axis))]).T
    m, c = np.linalg.lstsq(A, price, rcond=None)[0]
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
    price = np.flipud(df["<CLOSE>"].values)[70:100]
    x_axis = np.linspace(0, 1, price.size)
    price = price - np.min(price)
    price = price/np.max(price)
    detection, m, c = detect_trend(df, 70)
    y = m*x_axis + c
    print(detection)
    plt.plot(x_axis, y)
    plt.plot(x_axis, price)
    plt.show()
