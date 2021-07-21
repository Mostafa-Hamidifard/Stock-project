from receiving_and_cleaning import receive_data as rd
import os

if __name__ == '__main__':
    rd.start_downloading_data_and_store(
        "stocks.txt", store_path=os.path.join(os.getcwd(), "CSV raw data"))
