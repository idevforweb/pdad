import requests
import streamlit as st
import pandas as pd
import datetime
import os

from csv import DictReader
from pprint import pprint


st.set_page_config(
    layout="wide",
    page_title='Powerball Data Tool',
)

#
# Update powerball csv file
#


def update_csv_file():

    def download_csv_file():
        # URL of the powerball csv download file
        csv_url = requests.get('https://nclottery.com/powerball-download')
        # replace the csv file
        with open("powerball.csv", "wb")as csv_file:
            csv_file.write(csv_url.content)

    def todays_date():
        date = str(datetime.datetime.now()).split()[0]
        return date

    def powerball_file_date():
        date = str(datetime.datetime.fromtimestamp(
            os.path.getmtime('powerball.csv'))).split()[0]
        return date

    if os.path.exists('powerball.csv') == False:
        print("Downloadiing Powerball CSV Data")
        download_csv_file()
    elif todays_date() == powerball_file_date():
        print("Dates match")
    elif todays_date() != powerball_file_date():
        download_csv_file()
        print("Powerball csv file Updated")


update_csv_file()


#
# Power Ball Data
#


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


# Create Dataframe
df = pd.DataFrame(data())


def csv_last_updated():
    # get last csv update info
    date_data = str(datetime.datetime.fromtimestamp(
        os.path.getmtime('powerball.csv')))
    # get date
    date = date_data.split()[0].split('-')
    # get time
    time = date_data.split()[1].split('.')
    return {
        "last_updated": f'Last update: {date[1]}-{date[2]}-{date[0]} | {time[0]}.'
    }


win_precentage = 'total wins'

#
# side bar checkboxes
#

st.sidebar.subheader("Show Tables")
st.sidebar.write("")
show_recent_wins = st.sidebar.checkbox("Recent Win", value=True)
show_oldest_wins = st.sidebar.checkbox("Oldest Win", value=True)
show_all_numbers = st.sidebar.checkbox("All Numbers", value=True)
show_numbers_summary = st.sidebar.checkbox("Summary", value=True)


#
# Recent and oldest wins
#

if show_recent_wins:
    st.write("Most recent winning Numbers")
    st.write(df.head(1))  # get first row
if show_oldest_wins:
    st.write("Oldest winning numbers")
    st.write(df.tail(1))  # get first row


#
# Session States
#


def reset_data():
    st.session_state.switcher = 0
    st.session_state.input_date = ''
    st.session_state.input_number = ''
    st.session_state.total_number = 0


if 'df' not in st.session_state:
    st.session_state.switcher = 0
    st.session_state.input_date = ''
    st.session_state.input_number = ''
    st.session_state.total_number = 0
    st.session_state.win_percentage = 'win'

# st.session_state


def get_total_row_wins():
    number = st.session_state.total_number

    def make_int_arrays(col):
        array = [int(number) for number in df[col].values]
        win_percentage = st.session_state.win_percentage
        if win_percentage == 'win':
            return len([num for num in array if num == number])
        elif win_percentage == 'greater than':
            return len([num for num in array if num >= number])
        elif win_percentage == 'less than':
            return len([num for num in array if num <= number])

    n1 = make_int_arrays('Number 1')
    n2 = make_int_arrays('Number 2')
    n3 = make_int_arrays('Number 3')
    n4 = make_int_arrays('Number 4')
    n5 = make_int_arrays('Number 5')
    add_wins = n1 + n2 + n3 + n4 + n5
    get_percentage = (add_wins/len(df)) * 100
    data = {
        "Number 1": [n1],
        "Number 2": [n2],
        "Number 3": [n3],
        "Number 4": [n4],
        "Number 5": [n5],
        "Total Wins": [add_wins],
        "Percentage": [get_percentage]
    }
    return pd.DataFrame(data, index=[f"Number {number}  "])


st.write(f'Win percentage by number:  {st.session_state.total_number}')
st.write(get_total_row_wins())


def search_by_date():
    input_from_date = st.session_state.input_date
    if " " in input_from_date:
        st.session_state.input_date = ','.join(input_from_date.split(' '))
    date = st.session_state.input_date.split(',')
    st.session_state.switcher = 'date'
    st.session_state.input_number = ''
    if len(date[0]) == 4:
        return df.loc[df["Year"] == date[0]]
    elif len(date) == 1:
        return df.loc[df["Month"] == date[0]]
    elif len(date) == 2:
        return df.loc[(df["Month"] == date[0]) & (df["Day"] == date[1])]
    elif len(date) == 3:
        return df.loc[
            (df["Month"] == date[0])
            & (df["Day"] == date[1])
            & (df["Year"] == date[2])]


def search_by_number():
    input_from_numbers = st.session_state.input_number
    if " " in input_from_numbers:
        st.session_state.input_number = ','.join(input_from_numbers.split(' '))
    numbers = st.session_state.input_number.split(',')
    st.session_state.switcher = 'number'
    st.session_state.input_date = ''
    if numbers[0][0:1] == 'n' and len(numbers[0]) == 2:
        letters = numbers[0]
        numbers = numbers[1]
        columns = "Number 1"
        match letters:
            case 'n1': columns = "Number 1"
            case 'n2': columns = "Number 2"
            case 'n3': columns = "Number 3"
            case 'n4': columns = "Number 4"
            case 'n5': columns = "Number 5"
            case 'n6': columns = "Power Ball"
            case 'n7': columns = "Power Play"
            case default: columns = "Number 1"
        return df.loc[df[columns] == numbers]
    elif len(numbers) == 1:
        return df.loc[df["Number 1"] == numbers[0]]
    elif len(numbers) == 2:
        return df.loc[
            (df["Number 1"] == numbers[0]) &
            (df["Number 2"] == numbers[1])]
    elif len(numbers) == 3:
        return df.loc[
            (df["Number 1"] == numbers[0]) &
            (df["Number 2"] == numbers[1]) &
            (df["Number 3"] == numbers[2])]
    elif len(numbers) == 4:
        return df.loc[
            (df["Number 1"] == numbers[0]) &
            (df["Number 2"] == numbers[1]) &
            (df["Number 3"] == numbers[2]) &
            (df["Number 4"] == numbers[3])]
    elif len(numbers) == 5:
        return df.loc[
            (df["Number 1"] == numbers[0]) &
            (df["Number 2"] == numbers[1]) &
            (df["Number 3"] == numbers[2]) &
            (df["Number 4"] == numbers[3]) &
            (df["Number 5"] == numbers[4])]
    elif len(numbers) == 6:
        return df.loc[
            (df["Number 1"] == numbers[0]) &
            (df["Number 2"] == numbers[1]) &
            (df["Number 3"] == numbers[2]) &
            (df["Number 4"] == numbers[3]) &
            (df["Number 5"] == numbers[4]) &
            (df["Power Ball"] == numbers[5])]
    elif len(numbers) == 7:
        return df.loc[
            (df["Number 1"] == numbers[0]) &
            (df["Number 2"] == numbers[1]) &
            (df["Number 3"] == numbers[2]) &
            (df["Number 4"] == numbers[3]) &
            (df["Number 5"] == numbers[4]) &
            (df["Power Ball"] == numbers[5]) &
            (df["Power Play"] == numbers[6])]


if st.session_state.switcher == 0:
    if show_all_numbers:
        st.subheader("Numbers Data")
        st.session_state.df = st.dataframe(df)
    if show_numbers_summary:
        st.write("Summary")
        st.session_state.desc = st.dataframe(df.describe())

elif st.session_state.switcher == 'date':
    if show_all_numbers:
        st.write("Numbers Data")
        st.session_state.df = search_by_date()
        st.write(st.session_state.df)
    if show_numbers_summary:
        st.write("Summary")
        st.session_state.desc = st.dataframe(search_by_date().describe())

elif st.session_state.switcher == 'number':
    if show_all_numbers:
        st.write("Numbers Data")
        st.session_state.df = search_by_number()
        st.write(st.session_state.df)
    if show_numbers_summary:
        st.write("Summary")
        st.session_state.desc = st.dataframe(search_by_number().describe())


# st.line_chart(
#     df.describe(), x=['Number 1', 'Number 2', 'Number 3']
# )


#
# Sideber
#

st.sidebar.write("")
st.sidebar.subheader("Search Data")

date_search = st.sidebar.text_input(
    label='Search by date',
    label_visibility='collapsed',
    key='input_date',
    on_change=search_by_date,
    placeholder="Search by Date"
)

number_search = st.sidebar.text_input(
    label='Search by number',
    label_visibility='collapsed',
    key='input_number',
    on_change=search_by_number,
    placeholder='Search by Number'
)

st.sidebar.write("")
st.sidebar.subheader("Search by Win percentage")


#
# Sidebar Win Percentage
#
number_search = st.sidebar.number_input(
    label='Search by number',
    min_value=0,
    max_value=69,
    label_visibility='collapsed',
    key='total_number',
    on_change=get_total_row_wins,
    placeholder='Search by Number'
)

# total_wins_checkbox = st.sidebar.checkbox(
#     'Win Percentage',
#     value=True,
# )
# greater_checkbox = st.sidebar.checkbox(
#     'Equal to and greater than',
#     value=False,
# )
# if total_wins_checkbox:
#     st.session_state.win_percentage = 'win'

# if greater_checkbox:
#     st.session_state.win_percentage = 'greater than'

reset_btn = st.sidebar.button(
    label='Reset All Data',
    on_click=reset_data,

)

st.sidebar.write(csv_last_updated()['last_updated'])

# st.write(st.session_state)
