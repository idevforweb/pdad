import streamlit as st


# counter tut: https://www.youtube.com/watch?v=KseiSR0MCTI

l = [1, 2, 3]

if 'selected_numbers' not in st.session_state:
    st.session_state.selected_numbers = []
st.session_state


def printKey(args):
    st.session_state.selected_numbers.append(int(args))
    st.write(args)


for x in l:
    st.button(f'{x}', key=f'{x}', args=(f'{x}'), on_click=printKey)
