import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from indicator import Indicator




class MovingAve(Indicator):
    def __init__(self,raw_data, rate):
        Indicator.__init__(self, raw_data)
        self.rate = rate
        self.date = self.raw_data[:,0][::-1]
        self.price = self.raw_data[:,1][::-1]
    
    def calculate_mvaverage(self):
        mv_ave = np.convolve(self.price, np.ones(self.rate), 'valid') / self.rate
        return np.concatenate(([0 for i in range(self.rate-1)], mv_ave), axis=0)

    
    def plot(self):
        fig = plt.figure(1)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        # x = self.raw_data[:,0]
        y = self.calculate_mvaverage(self.price, self.weight)
        # ax.plot([1,2,3, 5, 6 ,8 , 10], [1.8,2.0,3.5, 0.0 , 8.9, 4.5, 2.7])
        ax.plot(np.linspace(0, 50, 243), y, 'r', np.linspace(0, 50, 243), self.pri, 'b')
        plt.show()
        
        

        



if __name__ == "__main__":
    
    # df = pd.read_csv("2400322364771558.csv")
    # x = df[["<DTYYYYMMDD>", "<HIGH>"]].values
    # y = x[:,1][::-1]
    # print(y)
    y = [1, 2, 3, 4, 5, 6, 7, 8]
    mv = MovingAve(y, 3)
    # mv.plot()
    print(mv.calculate_mvaverage(y, 3))




    
    



