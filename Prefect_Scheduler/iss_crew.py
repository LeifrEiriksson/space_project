import os
import sys

import pandas as pd
from prefect import flow
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

@flow
def crew_sender():

    crew_data = crew()
    connection_db(crew_data,"crew_iss_daily")

    print("Crew Data Updated!")



if __name__ == '__main__':

    crew_sender.serve(name='Crew_data', 
                      tags = ['Crew Data', 'ISS Crew', 'Daily'],
                      cron = '10 6 * * *')