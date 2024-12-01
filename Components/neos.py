import os
from datetime import datetime, timedelta

import pandas as pd
import requests


class NEOs():


    def __init__(self):
        
        self._date_ref = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        try:
            self.response = requests.get(f'https://www.neowsapp.com/rest/v1/feed?start_date={self._date_ref}&end_date={self._date_ref}&detailed=false', timeout=50)
            self.response.raise_for_status()
            self._neos = self.response.json()
        
        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            self._neos = None

        except ValueError as json_err:
            print(f"JSON Error: {json_err}")
            self._neos = None

    def neos_data(self):
    
        self.tuple_infos1 = ('id','name','is_potentially_hazardous_asteroid')
        self.tuple_infos2 = ('orbiting_body','close_approach_date', 'relative_velocity') #close approach 
        self.tuple_infos3 = ('estimated_diameter_min','estimated_diameter_max') #estimated diameter
        self.data_l = []

        self._neos_data  = self._neos['near_earth_objects'][self._date_ref]

        for f in range(self._neos['element_count']):
        
            dict_data = {}
            dict_data['ref_date'] = self._date_ref

            for i in self.tuple_infos1:
                dict_data[i] = self._neos_data[f][i]

            for i in self.tuple_infos2:
            
                if i == 'relative_velocity':
                    rv = ('kilometers_per_hour', 'kilometers_per_second')
                    for j in rv:
                        dict_data[j] = self._neos_data[f]['close_approach_data'][0][i][j]

                else:
                    dict_data[i] = self._neos_data[f]['close_approach_data'][0][i]

            for i in self.tuple_infos3:
                dict_data[f'{i}_meters'] = self._neos_data[f]['estimated_diameter']['meters'][i]

            self.data_l.append(dict_data)

        self.df = pd.DataFrame(self.data_l)
        self.df[self.df.columns[-4:]] = self.df[self.df.columns[-4:]].astype(str)
        self.df['is_potentially_hazardous_asteroid'] = self.df['is_potentially_hazardous_asteroid'].astype(str)
        self.df.rename(columns={'id':'neo_id'},inplace=True)
                
        return self.df