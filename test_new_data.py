import pandas as pd
from powerball_data import data

import streamlit as st

pd = pd.DataFrame({
    'Month': [data()['Month'][0]]
})
pd
pd.dtypes
