# python modules
import streamlit as st
import pandas as pd
import numpy as np

# app modules
from update_csv import download_csv, csv_last_updated
from powerball_data import data

st.set_page_config(layout="wide", page_title='PDAD')

# download new csv file
download_csv()

# Create Dataframe
df = pd.DataFrame(data())
df['Month'] = df['Month'].astype('str')


#
# SIDE BAR LAYOUT : TITLE
#

st.sidebar.title("PDAD")
st.sidebar.write("Powerball Data Analysis Dashboard")
st.sidebar.write(csv_last_updated()['last updated'])
st.sidebar.divider()


#
# SESSION STATES
#


#
# COMPONENTS: RECENT AND OLDEST
#


def oldest_and_recent_wins():
    st.sidebar.subheader("Show Recents")
    show_recent_wins = st.sidebar.checkbox(
        "Recent Winning numbers", value=True)
    show_oldest_wins = st.sidebar.checkbox(
        "Oldest Winning numbers", value=True)
    # create conditions
    if show_recent_wins:
        # UI elemeents
        st.subheader("Most recent winning numbers")
        # get first row
        st.dataframe(df.head(1).drop(
            ['Jackpot', 'Power Play'], axis=1), hide_index=True)
    if show_oldest_wins:
        # UI elemeents
        st.subheader("Oldest winning numbers")
        # get first row
        st.dataframe(df.tail(1).drop(
            ['Jackpot', 'Power Play'], axis=1), hide_index=True)


oldest_and_recent_wins()


#
# COMPONENT: WIN PERCENTAGE
#


def search_by_percentage():
    # Create function scope Session States
    if "total_number" not in st.session_state:
        st.session_state.total_number = 1
    if 'search_options' not in st.session_state:
        st.session_state.search_options = "Equal to"
    if 'table_text' not in st.session_state:
        st.session_state.table_text = "Equal to"

    # View Sesssion Sates
    # st.session_state

    # Create function scope Session state variables
    number = st.session_state.total_number
    option = st.session_state.search_options
    # create function scope variables
    table_text = "equal to"

    # call back

    def number_search_callback():
        def get_number_total(col):
            # turn strings data in dataframe columns into array of integers
            array = [int(num) for num in df[col].values]
            # conditionals: Create list from number selected, then get length of list
            if option == 'Equal to':
                return len([num for num in array if num == number])
            elif option == 'Greater than / Equal to':
                return len([num for num in array if num >= number])
            elif option == 'Less than / Equal to':
                return len([num for num in array if num <= number])

        def get_all_numbers(col):
            # turn strings data in dataframe columns into array of integers
            array = [int(num) for num in df[col].values]
            # conditionals: Create list from number selected, then get length of list
            if option == 'Greater than / Equal to':
                return [num for num in array if num >= number]
            elif option == 'Less than / Equal to':
                return len([num for num in array if num <= number])

        # store array lengths as totals in variables for percentage data columns
        n1 = get_number_total('Number 1')
        n2 = get_number_total('Number 2')
        n3 = get_number_total('Number 3')
        n4 = get_number_total('Number 4')
        n5 = get_number_total('Number 5')

        # store array list as totals in variables for percentage data columns
        n1_list = get_all_numbers('Number 1')
        n2_list = get_all_numbers('Number 2')
        n3_list = get_all_numbers('Number 3')
        n4_list = get_all_numbers('Number 4')
        n5_list = get_all_numbers('Number 5')

        # add all variables for total wins column
        add_wins = n1 + n2 + n3 + n4 + n5
        # get percentage
        get_percentage = (add_wins/(len(df) * 5)) * 100
        # Create data object
        data = {
            "Number 1": [n1],
            "Number 2": [n2],
            "Number 3": [n3],
            "Number 4": [n4],
            "Number 5": [n5],
            "Total Wins": [f'{add_wins}  out of  {len(df) * 5} '],
            "Percentage": [get_percentage]
        }
        data_list = {
            "Number 1": [n1_list],
            "Number 2": [n2_list],
            "Number 3": [n3_list],
            "Number 4": [n4_list],
            "Number 5": [n5_list]
        }

        # return data as a dataframe and rename index, and add summary data to object
        return {
            'percentage data': pd.DataFrame(data, index=[f"Number {number}  "]),
            'list data': pd.DataFrame(),
        }

    # conditions to change table-text for percentage table
    if option == "Equal to":
        table_text = 'equal to '
    if option == "Greater than / Equal to":
        table_text = 'greater than and equal to  '
    if option == "Less than / Equal to":
        table_text = 'less than and equal to  '

    #
    # Ui Elements
    #
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.subheader("Search Win percentage")
    # show / hide percentage data table checkbox
    show_percentage_data = st.sidebar.checkbox(
        "Show Percentage data", value=True)
    # select box
    search_options = st.sidebar.selectbox(
        label="test",
        options=(
            "Equal to",
            "Greater than / Equal to",
            "Less than / Equal to"
        ),
        label_visibility='collapsed',
        key='search_options',
    )
    # number input
    number_search = st.sidebar.number_input(
        label='Search by number',
        min_value=1,
        max_value=69,
        label_visibility='collapsed',
        key='total_number',
        on_change=number_search_callback,
        placeholder='Search by Number'
    )
    if show_percentage_data:
        # write precenage table-text and table to ui
        st.subheader(f'Win percentage {table_text}:  {number}')
        st.dataframe(
            number_search_callback()['percentage data'],
            width=900
        )


search_by_percentage()


#
# COMPONENT: SUMMARY DATA
#


def summary_data():
    # Create function scope Session States
    if "summary_number" not in st.session_state:
        st.session_state.summary_number = 1
    # View Sesssion Sates (Testing)
    # st.session_state
    # Create function scope Session state variables
    number = st.session_state.summary_number

    # Summary Data Callback
    def summary_callback():
        def summary(df_column):
            # get number description and remove "Jackpot" column
            return df[df[df_column] == str(number)].describe().drop(['Jackpot', 'Power Play'], axis=1).drop(['count']).astype('str')

        def full_summary(df_column):
            # get number description and remove "Jackpot" column
            return df[df[df_column] == str(number)].drop(['Jackpot', 'Power Play', 'Month', 'Day', 'Year', 'Power Ball'], axis=1).astype('str')

        # return data and add summary data to object
        return {
            'summary data 1': summary('Number 1'),
            'summary data 2': summary('Number 2'),
            'summary data 3': summary('Number 3'),
            'summary data 4': summary('Number 4'),
            'summary data 5': summary('Number 5'),
        }

    # Ui Elements
    # st.sidebar.write("")
    st.sidebar.subheader("Search number summary")
    # show / hide summary data checkbox
    show_slot_data = st.sidebar.checkbox(
        "Show summary data", value=True)
    # number input
    number_search = st.sidebar.number_input(
        label='Search by number',
        min_value=1,
        max_value=69,
        label_visibility='collapsed',
        key='summary_number',
        on_change=summary_callback,
        placeholder='Search Number'
    )
    if show_slot_data:
        # write summary tables to ui
        st.subheader(f'Number summary: {number}')
        st.dataframe(summary_callback()['summary data 1'], width=900)
        st.dataframe(summary_callback()['summary data 2'], width=900)
        st.dataframe(summary_callback()['summary data 3'], width=900)
        st.dataframe(summary_callback()['summary data 4'], width=900)
        st.dataframe(summary_callback()['summary data 5'], width=900)


summary_data()


#
#  COMPONENT: FULL NUMBER SUMMARY
#


def all_occurences():
    # Create function scope Session States
    if "occurence_number" not in st.session_state:
        st.session_state.occurence_number = 1
    if "occurence_df" not in st.session_state:
        st.session_state.occurence_df = 'Niow'

    def numbers_list():
        from collections import Counter
        number = st.session_state.occurence_number
        cols = ['Number 1', 'Number 2', 'Number 3', 'Number 4', 'Number 5']
        # function to remove unwanted columns,
        # create single dataframe and set input number

        def data(cols_list):
            return df[df[cols_list] == str(number)].drop(['Jackpot', 'Power Play', 'Month', 'Day', 'Year', 'Power Ball'], axis=1)
        # create all Dataframes using data() function
        # and get all values ( numbers ), in nested list
        # use sum to flatten list in new nested list, using empty []
        # use numpy to flatten into single list of numbers
        # Change all strings numbers to interger numbers using int()
        list_of_numbers = [int(number) for number in
                           list(np.concatenate(
                               sum([data(number_col).values.tolist() for number_col in cols], [])))]
        # count all instances of input number
        input_number_count = list_of_numbers.count(int(number))
        # list numbers removing all input number instances
        list_minus_input = [
            numbers for numbers in list_of_numbers if numbers != int(number)
        ]
        list_with_input = [numbers for numbers in list_of_numbers]
        # count_all_numbers
        total_numbers = len(set(list_minus_input))
        # count the numbers from list and create and ordered key:value list
        list_counter = sorted(
            Counter(list_minus_input).items(), key=lambda x: x[1]
        )
        list_counter_with_number = sorted(
            Counter(list_with_input).items(), key=lambda x: x[1]
        )
        # get all lotto numbers from list counter
        powerball_numbers = [lotto_number[0]
                             for lotto_number in list_counter]
        # get all occurences from list counter
        powerball_number_occurences = [occurences[1]
                                       for occurences in list_counter]
        # # Create Datafrane from numbers and occurences
        numbers_and_occurences = pd.DataFrame({
            "Number": powerball_numbers,
            'Occurences': powerball_number_occurences,
        })
        # Ui Elements
        return numbers_and_occurences
    numbers_list()
    # st.sidebar.write("")
    st.sidebar.subheader("Search number occurences")
    # show / hide summary data checkbox
    show_occurences = st.sidebar.checkbox(
        "Show occurences data", value=True)
    # number input
    number_search = st.sidebar.number_input(
        label='Search by number',
        min_value=1,
        max_value=69,
        label_visibility='collapsed',
        key='occurence_number',
        on_change=numbers_list,
        placeholder='Search Number'
    )
    if show_occurences:
        st.subheader("Number Occurences")
        st.session_state.occurence_df = numbers_list()
        st.session_state.occurence_df
        st.bar_chart(
            st.session_state.occurence_df,
            use_container_width=False,
            x='Number',
            width=900)


all_occurences()


#
# COMPONENT: ADVANCED SEARCH
#


def advanced_search():
    # Create function scope Session States
    if "input_date" not in st.session_state:
        st.session_state.input_date = ''
    if "input_number" not in st.session_state:
        st.session_state.input_number = ''
    if "switcher" not in st.session_state:
        st.session_state.switcher = 0
    if "desc" not in st.session_state:
        st.session_state.desc = ''
    if "data_desc" not in st.session_state:
        st.session_state.data_desc = ''

    # Search by Date Callback

    def search_by_date():
        input_from_date = st.session_state.input_date
        # if there is a "space" or "/" in user input
        # remove and add commas
        if " " in input_from_date:
            st.session_state.input_date = ','.join(input_from_date.split(' '))
        elif "/" in input_from_date:
            st.session_state.input_date = ','.join(input_from_date.split('/'))
        # create list using split at commas
        date = st.session_state.input_date.split(',')
        st.session_state.switcher = 'date'
        st.session_state.input_number = ''
        st.session_state.data_desc = 'Showing all numbers data.'
        st.session_state.df = df.drop(
            ['Jackpot', 'Power Play'], axis=1
        )

        if date[0] == 'all' or date[0] == 'All':
            st.session_state.switcher = 0
        if len(date[0]) == 4:
            st.session_state.data_desc = f'Showing data from {date[0]}.'
            return df.loc[df["Year"] == date[0]]
        elif len(date) == 1:
            st.session_state.data_desc = f'Showing data from month {date[0]}.'
            return df.loc[df["Month"] == date[0]].astype('str')
        elif len(date) == 2 and len(date[1]) == 4:
            st.session_state.data_desc = f'Showing data from {date[0]}/{date[1]}.'
            return df.loc[(df["Month"] == date[0]) & (df["Year"] == date[1])].astype('str')
        elif len(date) == 2:
            st.session_state.data_desc = f'Showing data from {date[0]}/{date[1]}.'
            return df.loc[(df["Month"] == date[0]) & (df["Day"] == date[1])].astype('str')
        elif len(date) == 3:
            st.session_state.data_desc = f'Showing data from {date[0]}/{date[1]}/{date[2]}.'
            return df.loc[
                (df["Month"] == date[0])
                & (df["Day"] == date[1])
                & (df["Year"] == date[2])].astype('str')
        else:
            st.session_state.data_desc = f'No data from found from input, please try again.'
            st.session_state.switcher = 0

    def search_by_number():
        input_from_numbers = st.session_state.input_number
        if " " in input_from_numbers:
            st.session_state.input_number = ','.join(
                input_from_numbers.split(' '))
        numbers = st.session_state.input_number.split(',')
        st.session_state.switcher = 'number'
        st.session_state.input_date = ''
        st.session_state.data_desc = 'Showing all numbers data.'
        if numbers[0] == 'all' or numbers[0] == 'All':
            st.session_state.switcher = 0
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
                case default: pass
            st.session_state.data_desc = f'Showing all data for {numbers} in {columns} slot.'
            return df.loc[df[columns] == numbers]
        elif len(numbers) == 1:
            st.session_state.data_desc = f'Showing number {numbers[0]} as Number 1'
            return df.loc[df["Number 1"] == numbers[0]]
        elif len(numbers) == 2:
            st.session_state.data_desc = f"Showing data for numbers {','.join(numbers)}."
            return df.loc[
                (df["Number 1"] == numbers[0]) &
                (df["Number 2"] == numbers[1])]
        elif len(numbers) == 3:
            st.session_state.data_desc = f"Showing data for numbers {','.join(numbers)}."
            return df.loc[
                (df["Number 1"] == numbers[0]) &
                (df["Number 2"] == numbers[1]) &
                (df["Number 3"] == numbers[2])]
        elif len(numbers) == 4:
            st.session_state.data_desc = f"Showing data for numbers {','.join(numbers)}."
            return df.loc[
                (df["Number 1"] == numbers[0]) &
                (df["Number 2"] == numbers[1]) &
                (df["Number 3"] == numbers[2]) &
                (df["Number 4"] == numbers[3])]
        elif len(numbers) == 5:
            st.session_state.data_desc = f"Showing data for numbers {','.join(numbers)}."
            return df.loc[
                (df["Number 1"] == numbers[0]) &
                (df["Number 2"] == numbers[1]) &
                (df["Number 3"] == numbers[2]) &
                (df["Number 4"] == numbers[3]) &
                (df["Number 5"] == numbers[4])]
        elif len(numbers) == 6:
            st.session_state.data_desc = f"Showing data for numbers {','.join(numbers)}."
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

    # UI Elements ##########

    st.sidebar.write('')
    st.sidebar.subheader("Advanced Search")
    # SIDE BAR CHECKBOXES
    show_all_numbers = st.sidebar.checkbox("Numbers data", value=True)
    show_numbers_summary = st.sidebar.checkbox("Summary", value=True)

    #
    # SIDE BAR CHECKBOXES
    #

    # Switch Numbers Data to default numbers data
    if st.session_state.switcher == 0:
        if show_all_numbers:
            st.subheader("Numbers Data")
            st.session_state.data_desc = 'Showing all Numbers Data.'
            st.write(st.session_state.data_desc)
            st.session_state.df = df.drop(
                ['Jackpot'], axis=1
            )
            st.dataframe(st.session_state.df, width=900)
        if show_numbers_summary:
            st.subheader("Data Summary")
            st.session_state.desc = df.describe().drop(
                ['Jackpot'], axis=1).astype('str')
            st.session_state.desc
    # Switch data to date numbers data
    if st.session_state.switcher == 'date':
        if show_all_numbers:
            st.subheader("Numbers Data")
            st.write(st.session_state.data_desc)
            st.session_state.df = search_by_date().drop(
                ['Jackpot'], axis=1
            )
            st.session_state.df["Month"].astype('str')
            st.dataframe(st.session_state.df, width=900)
        if show_numbers_summary:
            st.subheader("Data Summary")
            st.session_state.desc = st.dataframe(
                search_by_date().describe().drop(
                    ['Jackpot'], axis=1).astype('str')
            )
            st.session_state.desc
    # Switch data to input numbers data
    if st.session_state.switcher == 'number':
        if show_all_numbers:
            st.subheader("Numbers Data")
            st.write(st.session_state.data_desc)
            st.session_state.df = search_by_number().drop(
                ['Jackpot'], axis=1
            )
            st.session_state.df["Month"].astype('str')
            st.dataframe(st.session_state.df, width=900)
        if show_numbers_summary:
            st.subheader("Data Summary")
            st.session_state.desc = st.dataframe(
                search_by_number().describe().drop(
                    ['Jackpot'], axis=1).astype('str')
            )
            st.session_state.desc
    # DATE INPUT
    date_search = st.sidebar.text_input(
        label='Search by date',
        label_visibility='collapsed',
        key='input_date',
        on_change=search_by_date,
        placeholder="Search by Date"
    )
    # NUMBER INPUT
    number_search = st.sidebar.text_input(
        label='Search by number',
        label_visibility='collapsed',
        key='input_number',
        on_change=search_by_number,
        placeholder='Search by Number'
    )


advanced_search()


#
# CENTER LAYOUT FOOTER
#


st.divider()
total_years = str(len(list(set(df['Year']))))
st.write(
    f'All data and averages reflect the last {total_years} years of powerball wins. This tool is for data analysis using previous powerball numbers and does not guarantee or predict winning numbers.'
)
