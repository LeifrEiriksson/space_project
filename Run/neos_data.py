import os
import sys
from datetime import datetime, timedelta
from time import sleep

import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from Components.data_sender import connection_db
from Components.neos import NEOs


@retry(
    stop=stop_after_attempt(10),  
    wait=wait_exponential(multiplier=2, min=2, max=12) 
)

def neos():

    neos = NEOs().neos_data()

    if neos is None:
        raise ValueError("Failed to fetch crew NEO(s) data.")

    return neos 


if __name__ == '__main__':
    neos_data = neos()
    connection_db(neos_data,"neos_daily")