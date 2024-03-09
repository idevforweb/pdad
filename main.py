from fastapi import FastAPI
from pandas import pandas as pd
import csv

from powerball_data import data

# create dataframe
df = pd.DataFrame(data())

# convert df to csv
df.to_csv('powerball_export.csv', index=False)

'''
read the CSV file using the csv module. We can use the csv.DictReader class to read the file and store each row as a dictionary.
'''

with open('powerball_export.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    powerball_data = [row for row in reader]
    powerball_data.pop()
    # get_month = [x for x in powerball_data if x["Date"][0:2] == '02']


app = FastAPI()


@app.get('/{month}')
def get_all_numbers(month: str):
    # https://medium.com/swlh/3-alternatives-to-if-statements-to-make-your-python-code-more-readable-91a9991fb353
    date = month.split(',')
    if len(date) == 1:
        m = date[0]
        print(m)
    elif len(date) == 2:
        d = date[1]
        print(d)
    elif len(date) == 3:
        m = date[0]
        d = date[1]
        y = date[2]
        print(m, d, y)
        t = [x for x in powerball_data if
             x["Month"] == date[0] and
             x['Day'] == date[1] and
             x['Year'] == date[2]
             ]
    return {"data": t}
