import streamlit as st

key = 'is_processing_user_input'

def is_processing_user_input() -> bool:
    return st.session_state[key]


def set_processing_user_input(state: bool):
    st.session_state[key] = state


def init_processing_user_input():
    if key not in st.session_state:
        set_processing_user_input(False)
