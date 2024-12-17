import streamlit as st


def init_previous_if_empty():
    if 'previous' not in st.session_state:
        st.session_state['previous'] = {}
        st.session_state['previous']['audio'] = None


def save_previous_audio(audio):
    st.session_state['previous']['audio'] = audio


def get_previous_audio():
    return st.session_state['previous']['audio']
