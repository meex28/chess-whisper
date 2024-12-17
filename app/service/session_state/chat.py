from typing import List, Dict

import streamlit as st


def init_chat_state_if_empty():
    if 'chat_messages' not in st.session_state:
        st.session_state['chat_messages'] = []


def add_chat_message(role: str, content: str):
    init_chat_state_if_empty()

    st.session_state['chat_messages'].append({
        "role": role,
        "content": content
    })


def get_chat_messages() -> List[Dict[str, str]]:
    init_chat_state_if_empty()
    return st.session_state['chat_messages']


def clear_chat_history():
    st.session_state['chat_messages'] = []
