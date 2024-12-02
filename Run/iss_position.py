import os
import sys
from datetime import datetime, timedelta
from time import sleep

import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from Components.data_sender import connection_db
from Components.iss import Iss


@retry(
    stop=stop_after_attempt(10),  
    wait=wait_exponential(multiplier=2, min=2, max=12) 
)

def position():

    pos = Iss().iss_position()

    if pos is None or pos == 'Failed to connect.':
        raise ValueError("Failed to fetch ISS Position.")  
    return pos

def pos_sender():

    data_list = []

    for i in range(30):

        try:

            iss_pos = position()
            data_list.append(iss_pos)
            sleep(10)
            print('Data collect done!')

        except Exception as e:
            print(f"Error: {i} time: {str(e)}")
    
    iss_df = pd.DataFrame(data_list)

    iss_df['timestamp'] = pd.to_datetime(iss_df['timestamp'], unit = 's')
    iss_df['latitude'] = iss_df['latitude'].astype(str)
    iss_df['longitude'] = iss_df['longitude'].astype(str)
    iss_df['timestamp'] = iss_df['timestamp'].astype(str)
    iss_df.rename(columns={'timestamp':'date_hour_ref'},inplace = True)
    
    return iss_df


if __name__ == '__main__':

    data_pos = pos_sender()
    connection_db(data_pos,"iss_positions")
