import os
import sys
from datetime import datetime, timedelta
from time import sleep

import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from Components.data_sender import connection_db
from Components.flares import Flares


@retry(
    stop=stop_after_attempt(10),  
    wait=wait_exponential(multiplier=2, min=2, max=12) 
)

def flares():

    data_flares = Flares().flares_data()

    if data_flares is None:

        raise ValueError("Failed to fetch Flares data.")
    
    return data_flares


if __name__ == '__main__':

    flares_data = flares() 

    if flares_data.empty == True:
        print("Empty Data - Flares.")

    else:
        flares_data
        connection_db(flares_data,"crew_iss_daily")