import datetime
import json

import pandas as pd
import requests


class Iss():

    def __init__ (self):

        self.response_crew = requests.get("http://api.open-notify.org/astros.json")
        self.response_iss = requests.get("http://api.open-notify.org/iss-now.json")


    def crew_members (self):
        
        try:
            self.response_crew.raise_for_status()
            self.response_crew = self.response_crew.json()

        except requests.exceptions.RequestException as req_err:
            print(f"Request Error: {req_err}")
            self.response_crew = None

        except ValueError as json_err:
            print(f"JSON Error: {json_err}")
            self.response_crew = None

        if self.response_crew["message"] == "success":     

            self.crew = [names['name'] for names in self.response_crew['people'] if names['craft'] == 'ISS']
            self.df = pd.DataFrame({"name":self.crew})
            self.df["date_ref"] = datetime.datetime.today().strftime("%Y-%m-%d")

            return self.df
        
        else:
            return 'Failed to connect.'

    def iss_position (self):

        try:
            self.response_iss.raise_for_status()  
            self.response_iss = self.response_iss.json() 

        except requests.exceptions.RequestException as req_err:
            print(f"Request Error: {req_err}")
            self.response_iss = None

        except ValueError as json_err:
            print(f"JSON Error: {json_err}")
            self.response_iss = None


        if self.response_iss["message"] == "success": 
    
            self.position = self.response_iss['iss_position']
            self.position['NS'] = "North" if float(self.response_iss['iss_position']['latitude']) > 0 else "South"
            self.position['WE'] =  "East" if float(self.response_iss['iss_position']['longitude']) > 0 else "West"
            self.position['timestamp'] = self.response_iss['timestamp']

            return self.position
        
        else:
            return 'Failed to connect.'