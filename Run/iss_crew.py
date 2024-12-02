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

def crew():

    crew = Iss().crew_members()

    if crew is None:

        raise ValueError("Failed to fetch crew members.") 
    
    return crew


if __name__ == '__main__':

    crew_data = crew()
    connection_db(crew_data,"crew_iss_daily")