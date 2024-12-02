import os

import pandas as pd
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


def connection_db (dataframe,table_name):

    load_dotenv()
    
    conn = psycopg2.connect(
            host=os.getenv("PSQL_HOST"),
            port=os.getenv("PSQL_PORT"),
            database=os.getenv("PSQL_DATABASE"),
            user=os.getenv("PSQL_USER"),
            password=os.getenv("PSQL_PASSWORD")
        )

    if dataframe.empty == False:

        columns = ', '.join(dataframe.columns)
        values = [tuple(row) for row in dataframe.values]
        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES %s"

        try:
    
            cursor = conn.cursor()
            psycopg2.extras.execute_values(cursor, sql_insert, values)
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            conn.rollback()
            print(e)
            
    else: 
        print('Empty Dataframe!')