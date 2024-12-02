import os
import subprocess
import sys
from datetime import datetime

import luigi

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from Components.data_sender import connection_test


class ConnectionTestTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget('connection_test_output.txt') 

    def run(self):
        result = connection_test()[1]

        if result != 'ok':
            raise Exception("Connection failed!")
        
        else:
            with self.output().open('w') as f:
                f.write(f"Connection is OK at {datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}\n")


class IssCrewDataTask(luigi.Task):

    def requires(self):
        return ConnectionTestTask()

    def output(self):
        return luigi.LocalTarget('crew_output.txt')
    
    def run(self):
        script_path = os.path.join('..', 'Run', 'iss_crew.py')
        subprocess.run(['python', script_path], check=True)

        with self.output().open('w') as f:
                f.write(f"Data sending okay - ISS Crew - at {datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}\n")

if __name__ == '__main__':
    luigi.build([IssCrewDataTask()])