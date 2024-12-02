import os
import subprocess

import luigi


class ISSPositionTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget('iss_position_output.txt')
    
    def run(self):
        script_path = os.path.join('..', 'Run', 'iss_position.py')
        subprocess.run(['python', script_path], check=True)

if __name__ == '__main__':
    luigi.run()