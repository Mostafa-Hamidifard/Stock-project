from receiving_and_cleaning import receive_data
import os
receive_data.start_downloading_data_and_store(
    "stocks.txt", store_path=os.path.join(os.getcwd(), "CSV raw data"))
