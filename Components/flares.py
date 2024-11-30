import json
import os
from datetime import datetime, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv


class Flares():

    def __init__ (self):

        self._initialize()


    def _initialize(self): 

        self.__nasa_api_key = os.environ.get("NASA_API_KEY")
        self.__date_ref = (datetime.today()  - timedelta(days = 1)).strftime("%Y-%m-%d")

        try:
            self.response = requests.get(f"https://api.nasa.gov/DONKI/FLR?startDate={self.__date_ref}&endDate={self.__date_ref}&api_key={self.__nasa_api_key}", timeout = 50)
            self.response.raise_for_status()
            self._flares = self.response.json()
        
        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            self._flares = None

        except ValueError as json_err:
            print(f"JSON Error: {json_err}")
            self._flares = None

    def flares_data(self):

        try:

            self.rename_columns = {
            'flrID': 'flr_id',
            'instruments': 'instruments',
            'beginTime': 'begin_time',
            'peakTime': 'peak_time',
            'endTime': 'end_time',
            'classType': 'class_type',
            'sourceLocation': 'source_location',
            'activeRegionNum': 'active_region_num',
            'note': 'note',
            'submissionTime': 'submission_time',
            'versionId': 'version_id',
            'link': 'link',
            'linkedEvents': 'linked_events'}

            self.df = pd.DataFrame(self._flares)
            self.df = self.df.drop('catalog', axis = 1)

            self.df[["versionId"]] = self.df[["versionId"]].astype(str)
            self.df[["activeRegionNum"]] =  self.df[["activeRegionNum"]].astype(str)
            #self.df[["beginTime","peakTime","endTime","submissionTime"]] = self.df[["beginTime","peakTime","endTime","submissionTime"]].apply(pd.to_datetime)
            self.df['instruments'] = self.df['instruments'].apply(lambda x: json.dumps(x) if pd.notnull(x) else None)
            self.df['linkedEvents'] = self.df['linkedEvents'].apply(lambda x: json.dumps(x) if pd.notnull(x) else None)

            self.df.rename(columns = self.rename_columns, inplace=True)

            return self.df
        
        except:
            return pd.DataFrame()