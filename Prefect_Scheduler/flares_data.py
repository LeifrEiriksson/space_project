import os
import sys

import pandas as pd
from prefect import flow
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

@flow
def flares_sender():

    flares_data = flares() 

    if flares_data.empty == True:
        print("Empty Data - Theres no solar flares.")

    else:
        flares_data
        connection_db(flares_data,"flares_daily")
        print("Flares Data Updated!")


if __name__ == '__main__':

    flares_sender.serve(name='Flares_data', cron = '0 6 * * *')

