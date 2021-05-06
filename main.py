import pandas as pd
import requests
import os
import time
# from datetime import datetime

if __name__ == '__main__':
    path = os.getcwd()
    path = os.path.join(path, 'csvs')
    states = ['mx', 'in', 'it', 'nz', 'es']
    for state in states:
        dir_path = os.path.join(path, state)
        os.mkdir(dir_path)
        startdate = "01/05/2018"
        enddate = pd.to_datetime(startdate) + pd.DateOffset(days=7)
        while pd.to_datetime(startdate)<pd.to_datetime("12/31/2020"):
            csv_url = 'https://spotifycharts.com/regional/' + state + '/weekly/' + str(pd.to_datetime(startdate))[0:10]+'--'+str(enddate)[0:10] + '/download'
            req = requests.get(csv_url)
            print(req.status_code)
            time.sleep(1)
            if req.status_code == 200:
                url_content = req.content
                csv = '' + state + '_' + str(startdate)[0:10] + '.csv'
                csv_path = os.path.join(dir_path, csv)
                csv_file = open(csv_path, 'wb')

                csv_file.write(url_content)
                csv_file.close()

            else:
                print('error with the following file:' + str(csv_url))


            startdate = pd.to_datetime(enddate) + pd.DateOffset(days=1)
            enddate = pd.to_datetime(startdate) + pd.DateOffset(days=7)


