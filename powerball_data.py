import pandas as pd
from csv import DictReader
from pprint import pprint


def data():
    # convert csv column data to list dict and remove last row
    with open('powerball.csv', 'r') as powerball_csv_data:
        data = list(DictReader(powerball_csv_data))
        data.pop()

        # create helper functions
        def date(slice1, slice2):
            return [x["Date"][slice1:slice2] for x in data]

        def column_data(number_column):
            return [column[number_column] for column in data]

        return {
            'Month': date(0, 2),
            'Day': date(3, 5),
            'Year': date(6, 10),
            'Number 1': column_data('Number 1'),
            'Number 2': column_data('Number 2'),
            'Number 3': column_data('Number 3'),
            'Number 4': column_data('Number 4'),
            'Number 5': column_data('Number 5'),
            'Power Ball': column_data('Powerball'),
            'Power Play': column_data('Power Play'),
            'Jackpot': [x.split('.')[0] for x in column_data("Jackpot")],
        }
