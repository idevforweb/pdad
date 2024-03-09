import streamlit as st
import pandas as pd

from powerball_data import data

# create Dataframe
df_str = pd.DataFrame(data())
df_int = pd.read_csv('powerball.csv')

# remove additional .0000's
df_str['Jackpot'] = df_str["Jackpot"].str.split('.').str.get(0)

st.write("Frequent Winning Numbers")
st.dataframe(
    df_str.describe()
    .loc[['unique', 'top', 'freq']]
    .drop(['Month', 'Day', 'Jackpot', 'Year'], axis=1)
)

st.dataframe(df_int.describe().drop(['Jackpot'], axis=1))

st.write(f'All Wining Numbers')
st.dataframe(df_str.drop(['Jackpot'], axis=1))

st.dataframe(df_str.loc[df_str["Year"] == '2024'].describe())


st.dataframe(df_str.loc[
    (df_str["Number 1"] == '40') & (df_str["Number 2"] == '22')
])
st.dataframe(df_str.loc[(df_str["Number 1"] == '40')].describe())
