import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv


class Data_sender():

    def __init__(self,dataframe,table_name, conn=None):

        self.dataframe = dataframe
        self.table_name = table_name
        self.conn = conn
        self.cursor = None
    
    def connection(self):
        
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

        if not self.conn:
            self.conn = self.connection()

        if self.records.empty == False:

            self.columns = ', '.join(self.records.columns)
            self.values = [tuple(row) for row in self.records.to_records(index=False)]

            self.sql_insert = f"INSERT INTO {self.table_name} ({self.columns}) VALUES %s"

            try:
                if not self.cursor:
                    self.cursor = self.conn.cursor()
                    psycopg2.extras.execute_values(self.cursor, self.sql_insert, self.values)
                    self.conn.commit()

            except Exception as e:
                    self.conn.rollback()
                    return e


        else: 
            pass

    def close(self):
        
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()