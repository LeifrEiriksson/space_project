import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv


class Data_sender():

    def __init__(self,dataframe,table_name):

        self.dataframe = dataframe
        self.table_name = table_name
    
    def _connection(self):
        
        load_dotenv()

        try: 

            self.conn = psycopg2.connect(
                host=os.getenv("PSQL_HOST"),
                port=os.getenv("PSQL_PORT"),
                database=os.getenv("PSQL_DATABASE"),
                user=os.getenv("PSQL_USER"),
                password=os.getenv("PSQL_PASSWORD")
            )

            return self.conn

        except psycopg2.Error as error:
        
            print(f"database connection error: \n-- {error}\nplease try again!") 
    
    def sender(self):

        self.records = self.dataframe
        self.conn = self._connection()

        if self.records.empty == False:

            self.columns = ', '.join(self.records.columns)
            self.values = [tuple(row) for row in self.records.to_records(index=False)]

            self.sql_insert = f"INSERT INTO {self.table_name} ({self.columns}) VALUES %s"

            try:

                with self.conn.cursor() as cur:
                    
                    psycopg2.extras.execute_values(cur, self.sql_insert, self.values)
                    
                    self.conn.commit()
                    cur.close()
                    self.conn.close()

            except Exception as e:
                    self.conn.rollback()
                    return e


        else: 
            pass