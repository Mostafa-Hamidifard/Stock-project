import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from indicator import Indicator
from movingave import MovingAve

class BBolinger(Indicator):
    def __init__(self, raw_data):
        Indicator.__init__(self, raw_data)
        self.date = self.raw_data[:,0][::-1]
        self.price = self.raw_data[:,1][::-1]
    
    def calculate_BBolinger(self, weight):
        mv = MovingAve(self.raw_data, weight)
        sma = mv.calculate_mvaverage(self.raw_data, weight)
        # std = self.price.rolling(rate).std()
        print(sma)
        # bollinger_up = sma + std * 2 
        # bollinger_down = sma - std * 2 
        # return bollinger_up, bollinger_down
    
    def plot(self):
        pass


if __name__ == "__main__":
    df = pd.read_csv("2400322364771558.csv")
    x = df[["<DTYYYYMMDD>", "<HIGH>"]].values
    bb = BBolinger(x)
    # print(bb.calculate_BBolinger(20))
    bb.calculate_BBolinger(20)
    # print(bb.bollinger_down)

