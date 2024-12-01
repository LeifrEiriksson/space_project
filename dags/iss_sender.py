import os
import sys
from datetime import datetime, timedelta
from time import sleep

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from tenacity import retry, stop_after_attempt, wait_exponential

sys.path.append('/opt/airflow')

from Components.data_sender import Data_sender
from Components.iss import Iss

default_args = {
    'depends_on_past': False,
    'retries': 3,
    'start_date': datetime(2024, 11, 30),
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('iss_data_pipeline',
    default_args=default_args,
    description='ISS location - Pipeline',
    schedule_interval='*/30 * * * *', 
    tags = ['iss_location'],
    catchup=False) 

#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#

@retry(
    stop=stop_after_attempt(10),  
    wait=wait_exponential(multiplier=2, min=2, max=12) 
)

def position():

    pos = Iss().iss_position()

    if pos is None or pos == 'Failed to connect.':

        raise ValueError("Failed to fetch ISS Position.")  # Forçar nova tentativa
    
    return pos


def pos_sender():
    
    for i in range(30):

        try:

            iss_pos = position()
            sender = Data_sender([pd.DataFrame(iss_pos)],"iss_positions")
            sender.sender()
            
            sleep(30)


        except Exception as e:
            pass


#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#


positions_operator = PythonOperator(
    task_id='fetch_iss_positions_task',
    python_callable=pos_sender,
    dag=dag
)

positions_operator
