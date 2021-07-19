import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from indicator import Indicator

class MovingAve(Indicator):
    def __init__(self,raw_data, weight):
        Indicator.__init__(self, raw_data)
        self.weight = weight
    
    def calculate_mvaverage(self, data, weight):
        mv_ave = np.convolve(data, np.ones(weight), 'valid') / weight
        return np.concatenate(([0 for i in range(weight-1)], mv_ave), axis=0)
    
    def plot(self):
        fig = plt.figure(1)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        x = self.raw_data[:,0]
        y = self.calculate_mvaverage(self.raw_data[:,1], self.weight)
        # ax.plot([1,2,3, 5, 6 ,8 , 10], [1.8,2.0,3.5, 0.0 , 8.9, 4.5, 2.7])
        ax.plot(x, y, 'r', x, self.raw_data[:,1], 'b')
        plt.show()


        



if __name__ == "__main__":
    # data = np.array([10,5,8,9,15,22,26,11,15,16,18,7])
    # mv = MovingAve(data)
    # print(mv.calculate_mvaverage(4))
    df = pd.read_csv("65883838195688438.csv")
    x = df[["<DTYYYYMMDD>", "<HIGH>"]].values
    

   
    # plt.figure(1)
    # plt.plot(x,y)

    # ax.plot(x, y)
    # plt.show()


    # print(x[:,0])
    mv = MovingAve(x, 20)
    mv.plot()



    
    



