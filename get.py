from receiving_and_cleaning import receive_data as rd
import os
import pandas as pd
import numpy as np
from datetime import datetime



class ExtractCompaniesFeatures:
    def __init__(self, data_path_folder):
        self.data_path_folder = data_path_folder
        files = os.listdir(data_path_folder)
        self.all_compnies_data = {}
        for f in files:
            if f.endswith(".csv"):
                df = pd.read_csv(os.path.join(data_path_folder, f))[::-1]
                name = df["<TICKER>"].values[0]
                self.all_compnies_data[name] = df

    def get_company_names(self):
        return list(self.all_compnies_data.keys())
       

    def get_raw_price(self, company_name):
        df = self.all_compnies_data[company_name]
        return np.flip(df["<HIGH>"].values)
    
    def get_date(self, company_name):
        df = self.all_compnies_data[company_name]
        dates = np.flip(df["<DTYYYYMMDD>"].values)
        return [datetime.strptime(str(i), '%Y%m%d').strftime('%Y %m %d') for i in dates ]
    
   

    







if __name__ == '__main__':
    pass
    # rd.start_downloading_data_and_store(
    #     "stocks.txt", store_path=os.path.join(os.getcwd(), "CSV raw data"))
    # getDataName(os.path.join(os.getcwd(), "CSV raw data"))
    # inst = ExtractCompaniesFeatures(os.path.join(os.getcwd(), "CSV raw data"))
    # print(inst.get_row_price('G.Barekat.Pharm')[0])