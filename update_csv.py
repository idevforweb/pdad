import os
import datetime
import requests


def todays_date():
    return str(datetime.datetime.now()).split()[0]


def powerball_file_date():
    return str(datetime.datetime.fromtimestamp(
        os.path.getmtime('powerball.csv')))


def csv_last_updated():
    # get pb date
    date = powerball_file_date().split()[0].split('-')
    # get pb time
    time = powerball_file_date().split()[1].split('.')
    return {
        "last updated": f'Updated: {date[1]}-{date[2]}-{date[0]} | {time[0][:5]}'
    }

#


def download_csv():

    def download_csv_file():
        # URL of the powerball csv download file
        # replace the csv file
        csv_url = requests.get('https://nclottery.com/powerball-download')
        with open("powerball.csv", "wb") as csv_file:
            csv_file.write(csv_url.content)

    if os.path.exists('powerball.csv') == False:
        print("Downloading Powerball CSV Data")
        download_csv_file()
        return
    elif todays_date() == powerball_file_date().split()[0]:
        # print("Dates match")
        return
    elif todays_date() != powerball_file_date():
        download_csv_file()
        print("Powerball csv file Updated")
    else:
        print("Error: Powerball.csv was not able to be updated.")
